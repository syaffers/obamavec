cd ..

while read sp;
do
  grep -Eo "........................$sp:........................" raw2/*.txt
done < candidates.txt

echo "Check if there are new speakers in 'candidates.txt'"