#!/usr/bin/env python3
"""
Environment Diagnostics for Gemini API Handler
Provides comprehensive environment testing and validation
"""

import os
import sys
import json
import time
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnvironmentDiagnostics:
    """Comprehensive environment diagnostics for Gemini API Handler"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.results = {}
        
    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load configuration from file or environment"""
        default_config = {
            "required_dirs": [
                "/app/data",
                "/app/logs", 
                "/app/cache",
                "/tmp/gemini_api"
            ],
            "api_key_env": "GEMINI_API_KEY",
            "min_disk_space_mb": 100,
            "test_file_size_bytes": 1024,
            "timeout_seconds": 30
        }
        
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                default_config.update(loaded_config)
            except Exception as e:
                logger.warning(f"Failed to load config file {config_file}: {e}")
                
        # Override with environment variables
        env_dirs = os.environ.get('REQUIRED_DIRS', '').strip()
        if env_dirs:
            default_config['required_dirs'] = env_dirs.split()
            
        return default_config

    def run_full_diagnostic(self) -> Dict:
        """Run complete environment diagnostic suite"""
        logger.info("🚀 Starting Gemini API Handler Environment Diagnostics")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        # System information
        self.results['system'] = self._check_system_info()
        
        # Directory permissions
        self.results['directories'] = self._check_directory_permissions()
        
        # API configuration
        self.results['api_config'] = self._check_api_configuration()
        
        # Runtime environment
        self.results['runtime'] = self._check_runtime_environment()
        
        # Network connectivity (if applicable)
        self.results['network'] = self._check_network_connectivity()
        
        # Performance metrics
        self.results['performance'] = self._check_performance_metrics()
        
        elapsed_time = time.time() - start_time
        self.results['diagnostic_metadata'] = {
            'elapsed_time_seconds': round(elapsed_time, 2),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'config_used': self.config
        }
        
        # Generate summary
        self._generate_summary()
        
        logger.info("✅ Diagnostic suite completed")
        return self.results

    def _check_system_info(self) -> Dict:
        """Check basic system information"""
        logger.info("🖥️  Checking system information...")
        
        try:
            return {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'hostname': platform.node(),
                'user': os.environ.get('USER', 'unknown'),
                'uid': os.getuid() if hasattr(os, 'getuid') else None,
                'gid': os.getgid() if hasattr(os, 'getgid') else None,
                'working_directory': os.getcwd(),
                'environment_vars': {
                    key: value for key, value in os.environ.items() 
                    if 'GEMINI' in key or 'API' in key
                },
                'status': 'success'
            }
        except Exception as e:
            logger.error(f"System info check failed: {e}")
            return {'status': 'error', 'error': str(e)}

    def _check_directory_permissions(self) -> Dict:
        """Check directory permissions and disk space"""
        logger.info("📁 Checking directory permissions...")
        
        results = {
            'directories': {},
            'summary': {'total': 0, 'passed': 0, 'failed': 0},
            'status': 'success'
        }
        
        for directory in self.config['required_dirs']:
            results['summary']['total'] += 1
            dir_result = self._test_single_directory(directory)
            results['directories'][directory] = dir_result
            
            if dir_result['status'] == 'success':
                results['summary']['passed'] += 1
            else:
                results['summary']['failed'] += 1
                
        if results['summary']['failed'] > 0:
            results['status'] = 'partial_failure'
            
        return results

    def _test_single_directory(self, directory: str) -> Dict:
        """Test a single directory for all required permissions"""
        path = Path(directory)
        result = {
            'exists': False,
            'readable': False,
            'writable': False,
            'executable': False,
            'disk_space_mb': 0,
            'permissions': '',
            'owner': '',
            'group': '',
            'issues': [],
            'status': 'success'
        }
        
        try:
            # Check existence
            if path.exists():
                result['exists'] = True
                
                # Get file stats
                stat_info = path.stat()
                result['permissions'] = oct(stat_info.st_mode)[-3:]
                
                # Get owner/group info if available
                try:
                    import pwd
                    import grp
                    result['owner'] = pwd.getpwuid(stat_info.st_uid).pw_name
                    result['group'] = grp.getgrgid(stat_info.st_gid).gr_name
                except (ImportError, KeyError):
                    result['owner'] = str(stat_info.st_uid)
                    result['group'] = str(stat_info.st_gid)
                    
            else:
                # Try to create directory
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    result['exists'] = True
                    logger.info(f"  ✅ Created directory: {directory}")
                except Exception as e:
                    result['issues'].append(f"Cannot create directory: {e}")
                    result['status'] = 'error'
                    return result
            
            # Test read permission
            try:
                list(path.iterdir()) if path.is_dir() else path.read_text()
                result['readable'] = True
            except PermissionError:
                result['issues'].append("No read permission")
                
            # Test write permission
            test_file = path / f".write_test_{os.getpid()}"
            try:
                test_file.write_text("test")
                test_file.unlink()
                result['writable'] = True
            except PermissionError:
                result['issues'].append("No write permission")
            except Exception as e:
                result['issues'].append(f"Write test failed: {e}")
                
            # Test execute permission
            result['executable'] = os.access(str(path), os.X_OK)
            if not result['executable']:
                result['issues'].append("No execute permission")
                
            # Check disk space
            if path.exists():
                statvfs = os.statvfs(str(path))
                available_bytes = statvfs.f_frsize * statvfs.f_bavail
                result['disk_space_mb'] = round(available_bytes / (1024 * 1024), 2)
                
                if result['disk_space_mb'] < self.config['min_disk_space_mb']:
                    result['issues'].append(f"Low disk space: {result['disk_space_mb']}MB")
                    
        except Exception as e:
            result['issues'].append(f"Unexpected error: {e}")
            result['status'] = 'error'
            
        if result['issues']:
            result['status'] = 'error'
            
        return result

    def _check_api_configuration(self) -> Dict:
        """Check API key and configuration"""
        logger.info("🔐 Checking API configuration...")
        
        result = {
            'api_key_present': False,
            'api_key_valid_format': False,
            'api_key_source': None,
            'environment_vars': {},
            'status': 'success'
        }
        
        # Check for API key
        api_key_env = self.config['api_key_env']
        api_key = os.environ.get(api_key_env, '').strip()
        
        if api_key:
            result['api_key_present'] = True
            result['api_key_source'] = f"Environment variable: {api_key_env}"
            
            # Basic format validation (without revealing the key)
            if len(api_key) >= 20 and api_key.startswith(('AI', 'sk-', 'gsk_')):
                result['api_key_valid_format'] = True
            else:
                result['status'] = 'warning'
                
        else:
            result['status'] = 'error'
            
        # Collect relevant environment variables
        for key, value in os.environ.items():
            if any(term in key.upper() for term in ['GEMINI', 'API', 'TOKEN']):
                # Don't log actual secrets
                if 'KEY' in key.upper() or 'TOKEN' in key.upper():
                    result['environment_vars'][key] = '***' if value else 'NOT_SET'
                else:
                    result['environment_vars'][key] = value
                    
        return result

    def _check_runtime_environment(self) -> Dict:
        """Check runtime environment and dependencies"""
        logger.info("🔧 Checking runtime environment...")
        
        result = {
            'python_executable': sys.executable,
            'python_path': sys.path,
            'installed_packages': {},
            'mojo_available': False,
            'status': 'success'
        }
        
        # Check for key packages
        packages_to_check = ['requests', 'google-generativeai', 'anthropic']
        
        for package in packages_to_check:
            try:
                __import__(package)
                result['installed_packages'][package] = 'available'
            except ImportError:
                result['installed_packages'][package] = 'missing'
                
        # Check for Mojo
        try:
            subprocess.run(['mojo', '--version'], 
                         capture_output=True, 
                         timeout=self.config['timeout_seconds'])
            result['mojo_available'] = True
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            result['mojo_available'] = False
            
        return result

    def _check_network_connectivity(self) -> Dict:
        """Check network connectivity to API endpoints"""
        logger.info("🌐 Checking network connectivity...")
        
        result = {
            'endpoints': {},
            'dns_resolution': {},
            'status': 'success'
        }
        
        # Test endpoints
        endpoints_to_test = [
            'https://generativelanguage.googleapis.com',
            'https://aistudio.google.com',
            'https://ai.google.dev'
        ]
        
        for endpoint in endpoints_to_test:
            try:
                import socket
                from urllib.parse import urlparse
                
                parsed = urlparse(endpoint)
                hostname = parsed.hostname
                port = parsed.port or (443 if parsed.scheme == 'https' else 80)
                
                # DNS resolution test
                try:
                    ip = socket.gethostbyname(hostname)
                    result['dns_resolution'][hostname] = ip
                except socket.gaierror as e:
                    result['dns_resolution'][hostname] = f"Failed: {e}"
                    continue
                    
                # Connection test
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                
                if sock.connect_ex((hostname, port)) == 0:
                    result['endpoints'][endpoint] = 'reachable'
                else:
                    result['endpoints'][endpoint] = 'unreachable'
                    
                sock.close()
                
            except Exception as e:
                result['endpoints'][endpoint] = f"Error: {e}"
                
        return result

    def _check_performance_metrics(self) -> Dict:
        """Check system performance metrics"""
        logger.info("📊 Checking performance metrics...")
        
        result = {
            'memory_mb': 0,
            'cpu_count': 0,
            'load_average': [],
            'disk_io_test': {},
            'status': 'success'
        }
        
        try:
            # Memory info
            try:
                import psutil
                memory = psutil.virtual_memory()
                result['memory_mb'] = round(memory.total / (1024 * 1024), 2)
                result['memory_available_mb'] = round(memory.available / (1024 * 1024), 2)
                result['memory_percent_used'] = memory.percent
            except ImportError:
                # Fallback for systems without psutil
                pass
                
            # CPU info
            result['cpu_count'] = os.cpu_count()
            
            # Load average (Unix-like systems)
            try:
                result['load_average'] = list(os.getloadavg())
            except (AttributeError, OSError):
                pass
                
            # Simple disk I/O test
            test_dir = self.config['required_dirs'][0] if self.config['required_dirs'] else '/tmp'
            result['disk_io_test'] = self._perform_disk_io_test(test_dir)
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            
        return result

    def _perform_disk_io_test(self, test_dir: str) -> Dict:
        """Perform simple disk I/O performance test"""
        test_file = Path(test_dir) / f"io_test_{os.getpid()}.tmp"
        test_data = b"0" * self.config['test_file_size_bytes']
        
        result = {
            'write_speed_mbps': 0,
            'read_speed_mbps': 0,
            'status': 'success'
        }
        
        try:
            # Write test
            start_time = time.time()
            test_file.write_bytes(test_data)
            write_time = time.time() - start_time
            
            # Read test
            start_time = time.time()
            read_data = test_file.read_bytes()
            read_time = time.time() - start_time
            
            # Calculate speeds
            size_mb = len(test_data) / (1024 * 1024)
            result['write_speed_mbps'] = round(size_mb / write_time, 2) if write_time > 0 else 0
            result['read_speed_mbps'] = round(size_mb / read_time, 2) if read_time > 0 else 0
            
            # Verify data integrity
            if read_data != test_data:
                result['status'] = 'error'
                result['error'] = 'Data integrity check failed'
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        finally:
            # Cleanup
            try:
                test_file.unlink()
            except:
                pass
                
        return result

    def _generate_summary(self):
        """Generate diagnostic summary"""
        logger.info("📋 Generating diagnostic summary...")
        
        summary = {
            'overall_status': 'success',
            'critical_issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check each subsystem
        for subsystem, result in self.results.items():
            if subsystem == 'diagnostic_metadata':
                continue
                
            status = result.get('status', 'unknown')
            
            if status == 'error':
                summary['overall_status'] = 'error'
                summary['critical_issues'].append(f"{subsystem}: {result.get('error', 'Unknown error')}")
            elif status == 'partial_failure':
                if summary['overall_status'] != 'error':
                    summary['overall_status'] = 'warning'
                summary['warnings'].append(f"{subsystem}: Partial failure detected")
            elif status == 'warning':
                if summary['overall_status'] == 'success':
                    summary['overall_status'] = 'warning'
                summary['warnings'].append(f"{subsystem}: Warning detected")
                
        # Generate recommendations
        if not self.results.get('api_config', {}).get('api_key_present', False):
            summary['recommendations'].append("Set the GEMINI_API_KEY environment variable")
            
        if self.results.get('directories', {}).get('summary', {}).get('failed', 0) > 0:
            summary['recommendations'].append("Run init-directories.sh to fix directory permissions")
            
        if not self.results.get('runtime', {}).get('mojo_available', False):
            summary['recommendations'].append("Install Mojo runtime for optimal performance")
            
        self.results['summary'] = summary

    def print_report(self):
        """Print a formatted diagnostic report"""
        print("\n" + "=" * 70)
        print("🔍 GEMINI API HANDLER - ENVIRONMENT DIAGNOSTIC REPORT")
        print("=" * 70)
        
        # Summary
        summary = self.results.get('summary', {})
        status = summary.get('overall_status', 'unknown')
        status_emoji = {'success': '✅', 'warning': '⚠️', 'error': '❌'}.get(status, '❓')
        
        print(f"\n📊 OVERALL STATUS: {status_emoji} {status.upper()}")
        
        # Critical issues
        if summary.get('critical_issues'):
            print(f"\n❌ CRITICAL ISSUES:")
            for issue in summary['critical_issues']:
                print(f"  • {issue}")
                
        # Warnings
        if summary.get('warnings'):
            print(f"\n⚠️  WARNINGS:")
            for warning in summary['warnings']:
                print(f"  • {warning}")
                
        # Directory status
        dir_results = self.results.get('directories', {})
        if dir_results:
            print(f"\n📁 DIRECTORY STATUS:")
            for dir_path, dir_info in dir_results.get('directories', {}).items():
                status_emoji = '✅' if dir_info['status'] == 'success' else '❌'
                print(f"  {status_emoji} {dir_path}")
                if dir_info.get('issues'):
                    for issue in dir_info['issues']:
                        print(f"    ⚠️  {issue}")
                        
        # API Configuration
        api_config = self.results.get('api_config', {})
        if api_config:
            print(f"\n🔐 API CONFIGURATION:")
            api_key_status = '✅' if api_config.get('api_key_present') else '❌'
            print(f"  {api_key_status} API Key Present: {api_config.get('api_key_present', False)}")
            format_status = '✅' if api_config.get('api_key_valid_format') else '❌'
            print(f"  {format_status} API Key Format: {api_config.get('api_key_valid_format', False)}")
            
        # Recommendations
        if summary.get('recommendations'):
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(summary['recommendations'], 1):
                print(f"  {i}. {rec}")
                
        # Metadata
        metadata = self.results.get('diagnostic_metadata', {})
        print(f"\n📝 DIAGNOSTIC INFO:")
        print(f"  • Completed: {metadata.get('timestamp', 'Unknown')}")
        print(f"  • Duration: {metadata.get('elapsed_time_seconds', 'Unknown')}s")
        print(f"  • Hostname: {self.results.get('system', {}).get('hostname', 'Unknown')}")
        
        print("\n" + "=" * 70)

    def save_report(self, filename: str = 'diagnostic_report.json'):
        """Save diagnostic results to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            logger.info(f"📄 Diagnostic report saved to: {filename}")
        except Exception as e:
            logger.error(f"Failed to save report: {e}")

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gemini API Handler Environment Diagnostics')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--output', help='Output file for JSON report')
    parser.add_argument('--quiet', action='store_true', help='Reduce output verbosity')
    
    args = parser.parse_args()
    
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
        
    # Run diagnostics
    diagnostics = EnvironmentDiagnostics(args.config)
    results = diagnostics.run_full_diagnostic()
    
    # Print report
    diagnostics.print_report()
    
    # Save report if requested
    if args.output:
        diagnostics.save_report(args.output)
    else:
        diagnostics.save_report()
        
    # Exit with appropriate code
    overall_status = results.get('summary', {}).get('overall_status', 'unknown')
    if overall_status == 'error':
        sys.exit(1)
    elif overall_status == 'warning':
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()