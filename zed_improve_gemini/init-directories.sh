#!/bin/bash
# Dynamic directory initialization with permission fixing for Gemini API Handler
set -e

# Configuration
REQUIRED_DIRS="${REQUIRED_DIRS:-/app/data /app/logs /app/cache /tmp/gemini_api}"
DEFAULT_PERMS="${DEFAULT_PERMS:-755}"
CURRENT_USER=$(id -u)
CURRENT_GROUP=$(id -g)

echo "🚀 Initializing Gemini API Handler Environment"
echo "=" * 50
echo "Directories for user ${CURRENT_USER}:${CURRENT_GROUP}"

init_directory() {
    local dir="$1"
    local perms="${2:-${DEFAULT_PERMS}}"
    
    echo "📁 Processing: ${dir}"
    
    # Create directory if it doesn't exist
    if [ ! -d "${dir}" ]; then
        echo "  ➕ Creating directory: ${dir}"
        mkdir -p "${dir}"
    else
        echo "  ✅ Directory exists: ${dir}"
    fi
    
    # Fix ownership if we have permission
    if [ "$(stat -c '%u' "${dir}" 2>/dev/null || echo "")" != "${CURRENT_USER}" ] || [ "$(stat -c '%g' "${dir}" 2>/dev/null || echo "")" != "${CURRENT_GROUP}" ]; then
        echo "  🔧 Fixing ownership: ${CURRENT_USER}:${CURRENT_GROUP}"
        if chown "${CURRENT_USER}:${CURRENT_GROUP}" "${dir}" 2>/dev/null; then
            echo "  ✅ Ownership updated"
        else
            echo "  ⚠️  Cannot change ownership (may be read-only mount)"
        fi
    fi
    
    # Fix permissions
    echo "  🔒 Setting permissions: ${perms}"
    if chmod "${perms}" "${dir}" 2>/dev/null; then
        echo "  ✅ Permissions updated"
    else
        echo "  ⚠️  Cannot change permissions"
    fi
    
    # Verify write access
    local test_file="${dir}/.init_test_$$"
    if touch "${test_file}" 2>/dev/null; then
        rm -f "${test_file}"
        echo "  ✅ Directory is writable"
    else
        echo "  ❌ Directory is NOT writable"
        return 1
    fi
}

# Initialize all required directories
echo "🏗️  Initializing required directories..."
for dir in ${REQUIRED_DIRS}; do
    echo "----------------------------------------"
    init_directory "${dir}"
done

echo "----------------------------------------"
echo "✅ Directory initialization complete"

# Create a status file to indicate successful initialization
STATUS_FILE="/tmp/gemini_init_status"
echo "Environment initialized at $(date)" > "${STATUS_FILE}"
echo "📄 Status file created: ${STATUS_FILE}"

# Execute the main command if provided
if [ $# -gt 0 ]; then
    echo "🚀 Executing main command: $@"
    exec "$@"
else
    echo "🎯 Initialization complete - ready for API handler"
fi