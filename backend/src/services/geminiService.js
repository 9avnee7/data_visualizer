const { GoogleGenerativeAI } = require("@google/generative-ai");
require("dotenv").config();

class GeminiService {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.gemini_test_api_key);  // Use the correct environment variable
    // We assume that "gemini-2.0-flash" is the correct model identifier
    this.model = this.genAI.getGenerativeModel({ model: "gemini-2.0-flash" }); 
  }

  async generateTrace(code, template,algorithmName) {
    const prompt = `
Generate a ${algorithmName}'s algorithm trace for the following code:

CODE:
${code}

TEMPLATE REQUIREMENTS:
${JSON.stringify(template, null, 2)}

INSTRUCTIONS:
1. Use this default graph  for dijkstra algorithm if no graph is defined in the code:
   {
     "A": [["B", 4], ["C", 1]],
     "B": [["D", 1]],
     "C": [["B", 2], ["D", 5]],
     "D": []
   }
     keep this in mind
for bfs and dfs use this graph 
 {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "E"],
            "D": ["B"],
            "E": ["B", "C"]
        }

        and if the algorithm is quick sort and merge sort and input is not provided then take a 5 elements sample input array basic only
        do tracing of the input or defaut input according to the code provided to you it should be just like dry run
2. Start node: "A"

3. Generate a detailed trace of the algorithm execution, including all intermediate steps. Follow the TEMPLATE structure strictly.

4. Output must be a single object with four properties:
     - \`algorithmName\`: it must have the algorithm first name in lower case only
   - \`trace \`:an array of trace objects that simulate the step-by-step execution. accoeding to the input graph or array this should have proper dry run acc to the template we are passing to you
   - \`graph\`: the input graph used (either extracted from code or the default).
   -\ script\' : provude a textual script explaning the tracing steps in less then one minute take proper pausese also not too long just small pauses to be used for aws polly 
    keep the script up to the limit like it should not cross 50 seconds

Only return the variable declaration—no explanations, comments, or additional text.
`;

    try {
      // Generate content using the model
      const result = await this.model.generateContent({
        contents: [{ role: "user", parts: [{ text: prompt }] }]
      });

      const response = await result.response;
      const text = await response.text();

      // Clean up any markdown-style formatting if present
      let cleanedText = text.replace(/```[a-z]*\n/g, "").replace(/\n```/g, "");

      // Attempt to parse the cleaned response text as JSON
      try {
        const jsonResponse = JSON.parse(cleanedText);
        return jsonResponse;
      } catch (err) {
        console.error("Error parsing response as JSON:", err.message);
        throw new Error("Failed to parse response as JSON.");
      }
    } catch (err) {
      console.error("Error generating trace:", err.message);
      throw new Error("Failed to generate trace.");
    }
  }
}

module.exports = new GeminiService();
