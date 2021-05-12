echo "Ghetto Lint: helps find a small subset of syntax errors. Can be run locally."
echo "================= Checking bot.py " 
python3 -m py_compile bot.py
printf "import bot" | python3

# NOTE: can't do this cause myconstant import will mess things up ;-;
#for d in cogs/*.py ; do
#    echo "================= Checking $d"
#    python3 $d
#done