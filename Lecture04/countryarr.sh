count=0;fnr=0;IFS=$'\t';
read -p "What country shall we process the data for?" wantedcountry
inputfile="example_people_data.tsv"
inputfilelength=$(wc -l $inputfile | cut -d ' ' -f1)
outfile="Country.$wantedcountry.details"

rm -f *.details
unset my_array
declare -A my_array

while read name email city birthday_day birthday_month birthday_year country
do 
fnr=$((fnr+1))
# echo "Line number: $fnr"
if test -z $name || test $country == "country"
 then
 echo "" > /dev/null
 else
 if test $country == $wantedcountry
  then
  count=$((count+1))
  my_array[$count]="$fnr\t$name\t$country"
  # echo -e "${my_array[$count]}"
 fi
fi
# End of the file
if test $fnr -eq $inputfilelength
 then
 echo -e "\n### Here are the end of file results for $wantedcountry:" > $outfile
 for i in "${my_array[@]}"
  do
  echo -e "$i" >> $outfile
  done
fi
done < $inputfile
