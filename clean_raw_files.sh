if [ ! -d "processed" ]; then
  mkdir processed/
fi

cp raw/* processed/
cd processed/

echo "Removing starting brackets from start of file..."
for f in $(grep -l "^\]\s" *.txt)
do
  sed -i "s/^\]\s//" $f
done

echo "Removing everything between brackets..."
for f in $(grep -l "\[.*\?\]" *.txt)
do
  sed -i "s/\[[^]]*\]//g" $f
done

echo "Removing 'click for flash' text..."
for f in $(grep -l "click for flash" *.txt)
do
  sed -i "s/click for flash//g" $f
done

echo "Removing speaker tags..."
while read p
do
  for f in $(grep -l "$p:" *.txt)
  do
    sed -i "s/$p://g" $f
  done
done < ../speakers.txt

echo "Removing laughter..."
for f in $(grep -El "\([Ll]augh(s|ter).\)" *.txt)
do
  sed -i "s/\([Ll]augh(s|ter).\)//g" $f
done