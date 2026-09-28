# LOGICTREE_DIR="./GenerateSource"
# if [ ! -d "$LOGICTREE_DIR" ]; then
#   echo "Logic tree directory $LOGICTREE_DIR does not exist."
#   exit 1
# fi

file_list=()
file_list+=("temp/test_v1.jsonl")

# # echo "正在读取文件夹： $LOGICTREE_DIR"
# # for item in "$LOGICTREE_DIR"/*; do
# #   if [ -f "$item" ]; then
# #     file_list+=("$item")
# #     echo "找到文件: $item"
# #   fi
# # done

# echo "总共找到 ${#file_list[@]} 个文件。"
# printf "%s\n" "${file_list[@]}"

# prompt_v1_filelist=()
# prompt_v1_dir="./prompt_v1"
# for item in "${file_list[@]}"; do
#   if [ -e "$item" ]; then
#     filename=$(basename "$item" .jsonl)
#     outputname=${prompt_v1_dir}/"${filename}"_prompt_v1.jsonl
#     # python data_synthesis1_batch_hw.py $item $outputname
#     prompt_v1_filelist+=("$outputname")
#   fi
# done

# echo "总共生成 ${#prompt_v1_filelist[@]} 个 prompt_v1 文件。"
# printf "%s\n" "${prompt_v1_filelist[@]}"

# # python Chat_with_model_API_source1.py \
# #      --inputfilepaths ${prompt_v1_filelist[@]} 

process_v1_dir="./datav1/output"
process_v2_dir="./prompt_v2"

train_choice_list=()
for item in "${file_list[@]}"; do
    filename=$(basename "$item" .jsonl)
    inputname=${process_v1_dir}/"${filename}"_success.json
    outputname=${process_v1_dir}/"${filename}"_processed.jsonl
    python data_process1.py $inputname $outputname
    train_choice_name=${process_v2_dir}/"${filename}"_train_choice.jsonl
    # train_story_name=${process_v2_dir}/"${filename}"_train_story.jsonl
    python data_systhesis2_v1.py $outputname $train_choice_name
    # python data_systhesis2_v2.py $outputname $train_story_name
    train_choice_list+=("$train_choice_name")
    # train_choice_list+=("$train_story_name")
done


python Chat_with_model_API_source2.py \
    --inputfilepaths ${train_choice_list[@]}

result_dir="./result/output"
final_dir="./final"

for item in "${file_list[@]}"; do
    filename=$(basename "$item" .jsonl)
    train_choice_name=${result_dir}/"${filename}"_train_choice_success.json
    # train_story_name=${result_dir}/"${filename}"_train_story_success.json
    output1name=${final_dir}/"${filename}"_train_choice.jsonl
    # output2name=${final_dir}/"${filename}"_train_story.jsonl
    python Process_choice_output.py  $train_choice_name $output1name
    # cp $train_story_name $output2name
done