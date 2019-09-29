rm -f *.details
count=0
unset IFS
IFS=$'\t'
while read name email city birthday_day birthday_month birthday_year country
do
if test -z $name || test $country == "country"
 then
 continue
 else
 count=$((count+1))
 if test $birthday_month -eq 10
  then
  echo -e "$count\t$name\t$birthday_month\t$country" >> Month10.details
 fi
fi
done < example_people_data.tsv
