echo "Usage : bash filetune.sh API_KEY /path/to/jsonl_file MODEL_NAME"
echo "Model name can be : ada, babbage, curie, davinci. Each increasing in size and cost"

pip install --upgrade openai
export OPENAI_API_KEY=$1
openai tools fine_tunes.prepare_data -f $2
read -p "Enter the file id from above command: " FILE_ID
openai api fine_tunes.create -t $FILE_ID -m $3
read -p "Enter the finetune job id from above command: " FINE_TUNE_JOB_ID
openai api fine_tunes.follow -i $FINE_TUNE_JOB_ID
read -p "Enter the finetune model from above command: " FINE_TUNE_MODEL
echo "$FINE_TUNE_MODEL" > fine_tune_model.txt

read -p "Enter a prompt to test the model: " PROMPT
curl https://api.openai.com/v1/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": $PROMPT, "model": $FINE_TUNE_MODEL}'
