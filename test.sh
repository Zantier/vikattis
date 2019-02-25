folder=${1%/*}
echo -e "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
for in_file in $folder/*.in; do
	in=$(cat "$in_file")
	out=$(python3 "$1" < "$in_file")

	out_file=${in_file%.*}.ans
	expected=$(cat "$out_file")

	if [ "$out" != "$expected" ]; then
		echo in
		echo -e "$in"
		echo ''
		echo out
		echo -e "$out"
		echo ''
		echo expected
		echo -e "$expected"
		echo ''
		echo '--------------'
		echo ''
	fi
done
