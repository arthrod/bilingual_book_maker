# Commands

## Formatting texts to quarto

pdm run bbook_maker --book_name books/formatter/21F2_EN_test.md --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/formatter.prompt.md --batch_size=12 --single_translate --language en

## TSI_FI

# BM_IT

pdm run bbook_maker --book_name books/bm-it/ch01.qmd --model openai --model_list o3-mini --prompt prompts/it-translation.prompt.md --batch_size=5 --single_translate --language it

# BM_NL

pdm run bbook_maker --book_name books/bm-nl/to-edit --model openai --model_list o3-mini --prompt prompts/nl-edit-o3.prompt.md --batch_size=5 --single_translate --language nl --use_context --reasoning_effort=high

## 21FFF_FR

### Run 1

pdm run dir_process books/21fff/fr --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/fr-translation-2.prompt.md --batch_size=5 --single_translate --language fr

### Run 2

pdm run dir_process books/21fff/fr/to-edit --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/fr-edit-2.prompt.md --batch_size=5 --single_translate --language fr

## 21FFF_ES

pdm run dir_process books/21fff/es --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/es-translation-prompt.md --batch_size=5 --single_translate --language es

pdm run dir_process books/21fff/es/to-edit --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/es/es-edit.prompt.md --batch_size=5 --single_translate --language es