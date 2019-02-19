text=$(python3 submit/submit.py -f -l "Python 3" "$1" <<<'n')
echo text
echo -------
echo $text

regex='ID: (.*)\.'
if [[ "$text" =~ $regex ]]; then
	echo "${BASH_REMATCH[1]}" > "$(dirname "$1")/submission.txt";
else
	echo "Failed to create submission.";
fi
