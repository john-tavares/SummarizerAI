import tiktoken

SUMMARIZE_PROMPT = """
Atue como uma Inteligência Artificial curiosa e fofoqueira e leia este texto extraído de um {content_type}:
{text}
Gere um resumo objetivo e de fácil compreensão desse aúdio de WhatsApp, no idioma {language}.
Sempre referencie qualquer individuo como pessoa ou individuo e a pessoa que falou como individuo.
"""

YOUTUBE_PROMPT = """
Resuma este vídeo do Youtube:

Title: {video_title}
Channel: {video_channel}
Legenda: {video_caption}
"""

def generate_prompt(action:str, text:str, content_type:str, language:str="english")->str:
    if action == "summarize":
        base_prompt = SUMMARIZE_PROMPT

    prompt = base_prompt.format(content_type=content_type, text=text, language=language)
    return prompt

def generate_youtube_prompt(video:dict)->str:
    prompt = YOUTUBE_PROMPT.format(video_title=video['title'], video_channel=video['channel'], video_caption=video['captions'])
    return prompt

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")