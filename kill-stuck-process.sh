# This bash script can be used as a cronjob to kill all firefox and geckodrivers if the process has been stuck for more than 30 minutes.
lastfile=`ls ~/Human-Saliency-on-Snapshots-in-Web-Relevance/preprocessing/highlightGenerator/storage/highlights -t | head -1`
echo $lastfile

if test `find ~/Human-Saliency-on-Snapshots-in-Web-Relevance/preprocessing/highlightGenerator/storage/highlights/$lastfile -mmin +15`
then
    killall firefox
    killall geckodriver
fi
