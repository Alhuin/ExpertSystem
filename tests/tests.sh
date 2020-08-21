#!/bin/bash

FILES=$(find tests/examples/ -name "*.txt" | cut -d "/" -f 3- | tr "\n" " ")
IFS=$' ' read -r -a FILETAB <<< "$FILES"
for elem in "${FILETAB[@]}"
do
	echo ---------------------
	echo "examples$elem"
	PROGRAM=$(python3 main.py tests/examples/"$elem" | grep "# solution")
	SOLUTION=$(cat tests/examples$elem | grep "# solution")
	echo "$PROGRAM"
	if [ "$SOLUTION" = "$PROGRAM" ]; then
		echo -e "\033[32mOK\033[0m"
	else
		echo -e "\033[31mNOPE\033[0m"
	  echo "$SOLUTION"
	fi;
done


