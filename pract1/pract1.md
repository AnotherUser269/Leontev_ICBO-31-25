Task1:
```
#!/bin/bash
cat /etc/passwd | grep -o "^[^:]*" | sort
```

Task2:
```
#!/bin/bash
cat /etc/protocols | sort -rnk2 | grep -v "^#" | awk '{print $2, $1}' | head -n 5
```

Task3:
```
#!/bin/bash

textOfFrame="$1"
lenOfFrame=$(($(wc -c <<< "$textOfFrame")+1))

print_border() {
	printf "+"

	for((i=0; i<"$lenOfFrame"; i++)); do
		printf "-"
	done

	printf "+\n"
}

print_border
printf "| %s |\n" "$textOfFrame"
print_border
```

Task4:
```
#!/bin/bash
cat "$1" | grep -o "[A-Za-z_$][A-Za-z0-9_$]*" | sort | uniq
```

Task5:
#!/bin/bash
chmod +x "$1"
cp "$1" "$PREFIX/bin"
```

Task6:
```
#!/bin/bash

shopt -s nullglob globstar

for file in **/*.{c,js,py}; do
	firstLine="$(head -n 1 "$file")"

	# Python comment
	if [[ "$file" == *.py ]]; then
		if grep -q '^#' <<< "$firstLine"; then
			echo "$file"
		fi
	# .c comment
	elif [[ "$file" == *.c ]]; then
		if grep -qE '^(//|/\*)' <<< "$firstLine"; then
			echo "$file"
		fi
	# .js comment
	elif [[ "$file" == *.js ]]; then
                if grep -qE '^(//|/\*)' <<< "$firstLine"; then
                        echo "$file"
                fi
	fi

done
```

Task7:
```
shopt -s nullglob globstar

for i in **/*; do
	if [ -f "$i" ]; then
		md5sum "$i";
	fi
done | sort | uniq -w32 -D | tr -s ' ' | cut -d' ' -f2
```

Task8:
```
#!/bin/bash
tar cf "$(printf '%s' "$1" | tr -d '.')_file_archive.tar" -- *"$1"
```

Task9:
#!/bin/bash
sed 's/    /\t/g' < "$1" > "$2"
```

Task10:
```
#!/bin/bash

for file in "$1"/*; do
	if [ ! -s "$file" ] && grep -qEi "\.(docx|doc|txt)$" <<< "$file"; then 
		printf '%s\n' "$file"
	fi
done
```
