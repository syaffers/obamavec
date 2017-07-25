cd ..

while read sp;
do
  grep -Eo "........................$sp:........................" raw/*.txt | head -n 1 | awk '{split($0,a,":"); print a[2] a[3]}'
done < speakers.txt

echo "Check that all names are in 'speakers.txt'"