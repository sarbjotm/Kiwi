echo "Ghetto Lint: helps find a small subset of syntax errors. Can be run locally."
echo "================= Checking bot.py " 
python3 -m py_compile bot.py

for d in cogs/*.py ; do
    echo "================= Checking $d"
    python3 $d
done