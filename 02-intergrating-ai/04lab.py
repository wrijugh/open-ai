import semantic_kernel as sk
# import config.add_completion_service
from semantic_kernel import PromptTemplate, PromptTemplateConfig, SemanticFunctionConfig

from dotenv import dotenv_values
from semantic_kernel.connectors.ai.open_ai import (
    # OpenAIChatCompletion,
    AzureChatCompletion,
)

async def main():
    config = dotenv_values("../.env")
    deployment_type = config.get("AZURE_OPEN_AI__DEPLOYMENT_TYPE", None)

    # AzureOpenAI
    kernel = sk.Kernel(log=sk.NullLogger())
    kernel.add_chat_service(
        "chat_completion",
        AzureChatCompletion(
            deployment_name = config.get("AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME", None),
            endpoint = config.get("OPENAI_API_BASE", None),
            api_key = config.get("OPENAI_API_KEY", None),
        ),
    )

    prompt_config = PromptTemplateConfig(
        description="Gets the intent of the user.",
        type="completion",
        completion=PromptTemplateConfig.CompletionConfig(0.0, 0.0, 0.0, 0.0, 500),
        input=PromptTemplateConfig.InputConfig(
            parameters=[
                PromptTemplateConfig.InputParameter(
                    name="input", description="The user's request.", default_value="raspberry pi"
                )
            ]
        )
    )

    prompt = "What interesting things can I make with a {{$input}}?"

    prompt_template = PromptTemplate(
        template=prompt,
        template_engine= kernel.prompt_template_engine,
        prompt_config=prompt_config
    )
  
    
    function_config = SemanticFunctionConfig(
        prompt_template_config = prompt_config,
        prompt_template = prompt_template,
    )

    whatCanIMakeFunction = kernel.register_semantic_function(
        skill_name="Orchestration",
        function_name="WhatCanIMake",
        function_config=function_config,
    )

    result = await kernel.run_async(
        whatCanIMakeFunction,
        input_str="raspberry pi"
    )

    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())