set -e

# Run all .py files with patch_ prefix
# After running a file, move the file to ./scripts/trash
# and commit the changes (one commit per patch)

# Check if we are in the right directory
if [ ! -d "scripts" ]; then
    echo "Please run this script from the root directory of the repository"
    exit 1
fi

# Loop through all .py files with patch_ prefix
for file in $(ls scripts/patch_*.py); do
    echo "Running $file"
    python $file
    mv $file scripts/trash
    git add .
    git commit -m "Patch: $file"
done