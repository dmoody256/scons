cd ..
echo "$(find .circleci -name "*.txt" -print -exec cat {} \;)" > current.txt;
python3 runtest.py -l -a > all.txt;
grep -Fxv -f current.txt all.txt
rm current.txt all.txt
cd .circleci