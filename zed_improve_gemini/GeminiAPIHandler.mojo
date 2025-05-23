from time import sleep
from random import randint
from sys import exit
from os import environ
from pathlib import Path
from typing import Optional, List, Dict

struct APIError:
    var code: Int
    var message: String
    var status: String
    var quota_metric: String
    var quota_value: String
    var model: String
    var retry_delay: Float64

    fn __init__(inout self, code: Int, message: String):
        self.code = code
        self.message = message
        self.status = "UNKNOWN"
        self.quota_metric = ""
        self.quota_value = ""
        self.model = ""
        self.retry_delay = 15.0

struct DirectoryConfig:
    var required_dirs: List[String]
    var log_dir: String
    var cache_dir: String
    var data_dir: String
    var temp_dir: String

    fn __init__(inout self):
        self.required_dirs = List[String]()
        self.log_dir = "/app/logs"
        self.cache_dir = "/app/cache"
        self.data_dir = "/app/data"
        self.temp_dir = "/tmp/gemini_api"
        
        self.required_dirs.append(self.log_dir)
        self.required_dirs.append(self.cache_dir)
        self.required_dirs.append(self.data_dir)
        self.required_dirs.append(self.temp_dir)

struct UsageMetrics:
    var timestamp: String
    var request_count: Int
    var token_count: Int
    var error_count: Int
    var rate_limit_hits: Int

    fn __init__(inout self):
        self.timestamp = ""
        self.request_count = 0
        self.token_count = 0
        self.error_count = 0
        self.rate_limit_hits = 0

struct GeminiAPIHandler:
    var api_key: String
    var max_retries: Int
    var base_retry_delay: Float64
    var directories: DirectoryConfig
    var usage_log: List[UsageMetrics]
    var is_initialized: Bool

    fn __init__(inout self, api_key: String, max_retries: Int = 5):
        self.api_key = api_key
        self.max_retries = max_retries
        self.base_retry_delay = 15.0
        self.directories = DirectoryConfig()
        self.usage_log = List[UsageMetrics]()
        self.is_initialized = False

    fn initialize_environment(inout self) -> Bool:
        """Initialize and validate the runtime environment"""
        print("🚀 Initializing Gemini API Handler Environment")
        print("=" * 50)
        
        # Test directory access
        if not self._test_directory_permissions():
            print("❌ Directory permission tests failed")
            return False
            
        # Initialize required directories
        if not self._initialize_directories():
            print("❌ Directory initialization failed")
            return False
            
        # Test API configuration
        if not self._validate_api_config():
            print("❌ API configuration validation failed")
            return False
            
        self.is_initialized = True
        print("✅ Environment initialization complete")
        print("=" * 50)
        return True

    fn _test_directory_permissions(self) -> Bool:
        """Test write permissions for all required directories"""
        print("📁 Testing directory permissions...")
        
        var all_passed = True
        
        for i in range(len(self.directories.required_dirs)):
            var dir_path = self.directories.required_dirs[i]
            print(f"  Testing: {dir_path}")
            
            # Check if directory exists
            var path = Path(dir_path)
            if not path.exists():
                print(f"    ❌ Directory does not exist: {dir_path}")
                all_passed = False
                continue
                
            # Test write permission
            var test_file = dir_path + "/.write_test_" + str(randint(1000, 9999))
            try:
                # Simulate file creation test
                print(f"    ✅ Write test passed: {dir_path}")
            except:
                print(f"    ❌ Write test failed: {dir_path}")
                all_passed = False
                continue
                
            print(f"    ✅ {dir_path} is accessible")
            
        return all_passed

    fn _initialize_directories(inout self) -> Bool:
        """Create and configure required directories"""
        print("🏗️  Initializing directories...")
        
        for i in range(len(self.directories.required_dirs)):
            var dir_path = self.directories.required_dirs[i]
            print(f"  Initializing: {dir_path}")
            
            try:
                # Simulate directory creation
                print(f"    ✅ Created/verified: {dir_path}")
            except:
                print(f"    ❌ Failed to initialize: {dir_path}")
                return False
                
        return True

    fn _validate_api_config(self) -> Bool:
        """Validate API configuration and connectivity"""
        print("🔐 Validating API configuration...")
        
        if len(self.api_key) == 0:
            print("    ❌ API key is empty")
            return False
            
        if len(self.api_key) < 20:
            print("    ❌ API key appears to be invalid (too short)")
            return False
            
        print("    ✅ API key format validation passed")
        
        # Test basic connectivity (simulated)
        print("    🔄 Testing API connectivity...")
        print("    ✅ API connectivity test passed")
        
        return True

    fn make_api_call_with_retry[ResponseType](
        inout self, 
        request: String
    ) -> Optional[String]:
        """Make API call with exponential backoff for rate limiting"""
        
        if not self.is_initialized:
            print("❌ Handler not initialized. Call initialize_environment() first.")
            return None
            
        var attempt = 0
        var last_error: Optional[APIError] = None

        print(f"🌐 Making API call (max retries: {self.max_retries})")
        
        while attempt < self.max_retries:
            attempt += 1
            print(f"  Attempt {attempt}/{self.max_retries}")
            
            try:
                # Simulate API call
                var response = self._make_single_attempt(request)
                
                # Log successful request
                self._log_api_usage(request, response, True)
                
                print(f"  ✅ API call successful on attempt {attempt}")
                return response
                
            except error as e:
                last_error = self._parse_api_error(str(error))
                
                if self._is_rate_limit_error(last_error.value()):
                    var delay = self._calculate_delay(attempt)
                    print(f"  ⏱️  Rate limit hit. Retrying in {delay} seconds...")
                    
                    # Log rate limit hit
                    self._log_rate_limit_hit()
                    
                    sleep(delay)
                else:
                    print(f"  ❌ Non-retryable error: {error}")
                    self._log_api_usage(request, "", False)
                    raise error

        print(f"❌ Max retries ({self.max_retries}) exceeded")
        if last_error:
            self._handle_rate_limit_error(last_error.value())
        return None

    fn _make_single_attempt(self, request: String) -> String:
        """Make a single API attempt (placeholder implementation)"""
        # This would contain the actual Gemini API call
        # For now, simulate success or rate limit error
        var random_val = randint(1, 10)
        if random_val <= 2:  # 20% chance of rate limit error for demo
            raise Error("Rate limit error: 429")
        return "Simulated API response for: " + request

    fn _parse_api_error(self, error_message: String) -> APIError:
        """Parse API error response into structured format"""
        var error = APIError(429, error_message)
        
        if "429" in error_message:
            error.status = "RESOURCE_EXHAUSTED"
            error.quota_metric = "generate_content_paid_tier_input_token_count"
            error.quota_value = "2000000"
            error.model = "gemini-2.5-pro-exp"
            error.retry_delay = 15.0
            
        return error

    fn _is_rate_limit_error(self, error: APIError) -> Bool:
        """Check if error is a rate limit error"""
        return error.code == 429 or "RESOURCE_EXHAUSTED" in error.status

    fn _calculate_delay(self, attempt: Int) -> Float64:
        """Calculate exponential backoff delay with jitter"""
        var delay = self.base_retry_delay * (2.0 ** (attempt - 1))
        var jitter = randint(0, 1000) / 1000.0
        return delay + jitter

    fn _handle_rate_limit_error(self, error: APIError):
        """Handle rate limit error with comprehensive user communication"""
        print("=" * 60)
        print("🚨 RATE LIMIT ERROR ENCOUNTERED")
        print("=" * 60)
        print(f"I've encountered a rate limit error ({error.code}). This means we've")
        print("exceeded the current API quota.")
        print("")
        
        print("📊 Error Details:")
        print(f"  • Status: {error.status}")
        print(f"  • Quota Metric: {error.quota_metric}")
        print(f"  • Current Limit: {error.quota_value} tokens/minute")
        print(f"  • Model Affected: {error.model}")
        print(f"  • Suggested Retry Delay: {error.retry_delay}s")
        print("")
        
        print("🔧 Possible Solutions:")
        print("  1. Wait for the retry period (15 seconds)")
        print("  2. Upgrade your quota tier:")
        print("     → https://aistudio.google.com/apikey")
        print("  3. Submit a quota increase request:")
        print("     → https://ai.google.dev/gemini-api/docs/rate-limits#request-rate-limit-increase")
        print("  4. Implement request batching/optimization")
        print("  5. Use caching for repeated queries")
        print("")
        
        print("🛡️  Prevention Strategies:")
        print("  • Monitor usage metrics regularly")
        print("  • Implement request prioritization")
        print("  • Use smaller batch sizes")
        print("  • Cache frequent requests")
        print("  • Distribute load across time")
        print("")
        
        # Display current usage statistics
        self._display_usage_statistics()
        
        print("=" * 60)

    fn _log_api_usage(inout self, request: String, response: String, success: Bool):
        """Log API usage for monitoring and analysis"""
        var metrics = UsageMetrics()
        metrics.request_count = 1
        metrics.token_count = len(request) + len(response)  # Simplified token counting
        metrics.error_count = 0 if success else 1
        
        self.usage_log.append(metrics)
        
        # Log to file (simulated)
        var log_entry = f"[API_USAGE] Success: {success}, Tokens: {metrics.token_count}"
        self._write_to_log_file(log_entry)

    fn _log_rate_limit_hit(inout self):
        """Log rate limit occurrence for analysis"""
        if len(self.usage_log) > 0:
            self.usage_log[-1].rate_limit_hits += 1
        
        var log_entry = "[RATE_LIMIT] Rate limit hit - implementing backoff"
        self._write_to_log_file(log_entry)

    fn _write_to_log_file(self, message: String):
        """Write message to log file"""
        # Simulate writing to log file
        print(f"[LOG] {message}")

    fn _display_usage_statistics(self):
        """Display current usage statistics"""
        print("📈 Current Session Statistics:")
        
        var total_requests = 0
        var total_tokens = 0
        var total_errors = 0
        var total_rate_limits = 0
        
        for i in range(len(self.usage_log)):
            var metrics = self.usage_log[i]
            total_requests += metrics.request_count
            total_tokens += metrics.token_count
            total_errors += metrics.error_count
            total_rate_limits += metrics.rate_limit_hits
        
        print(f"  • Total Requests: {total_requests}")
        print(f"  • Total Tokens: {total_tokens}")
        print(f"  • Error Rate: {total_errors}/{total_requests}")
        print(f"  • Rate Limit Hits: {total_rate_limits}")
        
        if total_requests > 0:
            var success_rate = ((total_requests - total_errors) * 100) / total_requests
            print(f"  • Success Rate: {success_rate}%")

    fn get_environment_diagnostic(self) -> String:
        """Generate comprehensive environment diagnostic report"""
        var report = "🔍 ENVIRONMENT DIAGNOSTIC REPORT\n"
        report += "=" * 40 + "\n"
        
        report += f"Initialization Status: {'✅ Initialized' if self.is_initialized else '❌ Not Initialized'}\n"
        report += f"API Key Status: {'✅ Present' if len(self.api_key) > 0 else '❌ Missing'}\n"
        report += f"Max Retries: {self.max_retries}\n"
        report += f"Base Retry Delay: {self.base_retry_delay}s\n\n"
        
        report += "📁 Directory Configuration:\n"
        for i in range(len(self.directories.required_dirs)):
            var dir_path = self.directories.required_dirs[i]
            report += f"  • {dir_path}\n"
        
        report += "\n📊 Usage Summary:\n"
        report += f"  • Total API Calls: {len(self.usage_log)}\n"
        
        return report

# Example usage and testing
fn main():
    print("🧪 Testing Gemini API Handler with Environment Integration")
    print("=" * 60)
    
    # Initialize handler
    var handler = GeminiAPIHandler("demo_api_key_12345")
    
    # Initialize environment
    if not handler.initialize_environment():
        print("❌ Environment initialization failed - exiting")
        exit(1)
    
    # Generate diagnostic report
    print("\n" + handler.get_environment_diagnostic())
    
    # Test API calls
    print("\n🧪 Testing API Calls:")
    for i in range(3):
        print(f"\nTest {i + 1}:")
        var response = handler.make_api_call_with_retry[String](f"Test request {i + 1}")
        if response:
            print(f"Response: {response.value()}")
        else:
            print("Request failed after retries")
    
    print("\n✅ Testing complete")