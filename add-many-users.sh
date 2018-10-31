if [[ $# -ne 1 ]]
then
    echo "Script should receive a single argument: the contest id"
    echo "User Pass pairs are supplied through standard input"
    echo "Input is space separated, so usernames and passwords must not contain spaces"
    exit
fi

echo "Adding users to ContestID" $1

while read user pass
do
    cmsAddUser -p $pass $user "" $user
    cmsAddParticipation -c $1 $user
done
