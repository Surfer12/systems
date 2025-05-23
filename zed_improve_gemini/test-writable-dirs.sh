#!/bin/bash
# Permission tester for Gemini API Handler directories
set -e

DIRS_TO_TEST="${WRITABLE_DIRS:-/app/data /app/logs /app/cache /tmp/gemini_api}"
CURRENT_USER=$(id -u)
CURRENT_GROUP=$(id -g)

echo "🔍 DIRECTORY PERMISSION TESTING"
echo "=" * 40
echo "Testing for user ${CURRENT_USER}:${CURRENT_GROUP}"
echo "Directories to test: ${DIRS_TO_TEST}"
echo ""

test_directory() {
    local DIR="$1"
    local issues=0
    
    echo "📁 Testing: ${DIR}"
    echo "  $(ls -ld "${DIR}" 2>/dev/null || echo "Directory not found")"
    
    # Check if directory exists
    if [ ! -d "${DIR}" ]; then
        echo "  ❌ Directory does not exist: ${DIR}"
        return 1
    fi
    
    # Test read permission
    if ls "${DIR}" >/dev/null 2>&1; then
        echo "  ✅ Read permission: OK"
    else
        echo "  ❌ Read permission: FAILED"
        issues=$((issues + 1))
    fi
    
    # Test write permission
    TEST_FILE="${DIR}/.write_test_$$"
    if touch "${TEST_FILE}" 2>/dev/null; then
        echo "  ✅ Write permission: OK"
        rm -f "${TEST_FILE}"
    else
        echo "  ❌ Write permission: FAILED"
        issues=$((issues + 1))
    fi
    
    # Test execute permission (for directory traversal)
    if [ -x "${DIR}" ]; then
        echo "  ✅ Execute permission: OK"
    else
        echo "  ❌ Execute permission: FAILED"
        issues=$((issues + 1))
    fi
    
    # Check disk space
    local available_space=$(df -h "${DIR}" | tail -1 | awk '{print $4}')
    echo "  💾 Available space: ${available_space}"
    
    if [ ${issues} -eq 0 ]; then
        echo "  ✅ ${DIR} is fully accessible"
        return 0
    else
        echo "  ❌ ${DIR} has ${issues} permission issues"
        return 1
    fi
}

# Test all directories
failed_dirs=0
total_dirs=0

for DIR in ${DIRS_TO_TEST}; do
    echo "----------------------------------------"
    total_dirs=$((total_dirs + 1))
    
    if ! test_directory "${DIR}"; then
        failed_dirs=$((failed_dirs + 1))
    fi
    echo ""
done

echo "----------------------------------------"
echo "📊 TESTING SUMMARY"
echo "Total directories tested: ${total_dirs}"
echo "Failed directories: ${failed_dirs}"
echo "Success rate: $(( (total_dirs - failed_dirs) * 100 / total_dirs ))%"

if [ ${failed_dirs} -eq 0 ]; then
    echo "✅ All directory permission tests passed"
    exit 0
else
    echo "❌ ${failed_dirs} directories failed permission tests"
    echo ""
    echo "🔧 Suggested fixes:"
    echo "  1. Run the init-directories.sh script"
    echo "  2. Check Docker/Kubernetes volume mounts"
    echo "  3. Verify container user permissions"
    echo "  4. Ensure directories are not read-only"
    exit 1
fi