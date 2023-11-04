//dotnet add package dotenv.net --version 3.1.2
using dotenv.net;

//dotnet add package Microsoft.SemanticKernel --version 1.0.0-beta4
using Microsoft.SemanticKernel;

var envVars = DotEnv.Fluent()
    .WithoutExceptions()
    .WithEnvFiles(".env")
    .WithTrimValues()
    .WithDefaultEncoding()
    .WithOverwriteExistingVars()
    .WithoutProbeForEnv()
    .Read();

var model = envVars["AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME"].Replace("\"", "");
var azureEndpoint = envVars["OPENAI_API_BASE"].Replace("\"", "");
var apiKey = envVars["OPENAI_API_KEY"].Replace("\"", "");
// System.Console.WriteLine($"model: {apiKey}");

var builder = new KernelBuilder();
builder.WithAzureChatCompletionService(model, azureEndpoint, apiKey);
IKernel kernel = builder.Build();

string prompt = @"What interesting things can I make with a {{$input}}?";

var whatCanIMakeFunction = kernel.CreateSemanticFunction(prompt);

//string txt = "I want to send an email to the marketing team celebrating their recent milestone.";
var result = await kernel.RunAsync(
     "raspberry pi",
    whatCanIMakeFunction
);

Console.WriteLine(result);