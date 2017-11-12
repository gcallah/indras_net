
# Rscript post_process.r data_dir output_dir
summary_file_extension="_summary.txt"
rm mppref1.*/*$summary_file_extension

data_dir="mppref1.0"
output_dir="mppref1.0"
Rscript post_process.r $data_dir $output_dir;
vim -c ":%s/://g" -c ":%s/Qu.//g" -c "wq" "$data_dir/$output_dir$summary_file_extension";
awk '/Min/ { sum += $2; n++ } END { if (n > 0) print (sum / n); }' "$data_dir/$output_dir$summary_file_extension" > "trial.txt";
awk '/1st/ { sum += $2; n++ } END { if (n > 0) print (sum / n); }' "$data_dir/$output_dir$summary_file_extension" >> "trial.txt";
awk '/Median/ { sum += $2; n++ } END { if (n > 0) print (sum / n); }' "$data_dir/$output_dir$summary_file_extension" >> "trial.txt";
awk '/3rd/ { sum += $2; n++ } END { if (n > 0) print (sum / n); }' "$data_dir/$output_dir$summary_file_extension" >> "trial.txt";
awk '/Max/ { sum += $2; n++ } END { if (n > 0) print (sum / n); }' "$data_dir/$output_dir$summary_file_extension" >> "trial.txt";

data_dir="mppref1.2"
output_dir="mppref1.2"
Rscript post_process.r $data_dir $output_dir;
vim -c ":%s/://g" -c ":%s/Qu.//g" -c "wq" "$data_dir/$output_dir$summary_file_extension";

data_dir="mppref1.4"
output_dir="mppref1.4"
Rscript post_process.r $data_dir $output_dir;
vim -c ":%s/://g" -c ":%s/Qu.//g" -c "wq" "$data_dir/$output_dir$summary_file_extension";

data_dir="mppref1.6"
output_dir="mppref1.6"
Rscript post_process.r $data_dir $output_dir;
vim -c ":%s/://g" -c ":%s/Qu.//g" -c "wq" "$data_dir/$output_dir$summary_file_extension";

data_dir="mppref1.8"
output_dir="mppref1.8"
Rscript post_process.r $data_dir $output_dir;
vim -c ":%s/://g" -c ":%s/Qu.//g" -c "wq" "$data_dir/$output_dir$summary_file_extension";

# use awk script to process data
