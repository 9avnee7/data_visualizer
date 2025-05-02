const GeminiService = require("../services/geminiService")

const fs = require('fs');
// controllers/validateController.js
require('dotenv').config();
const logger=require('../utils/logger')

const { exec } = require('child_process');
const path = require('path');

const template=require('../utils/template')




const handleCodeValidation = (req, res) => {
  logger.info("Validation endpoint hit");

  try {
    const { algorithmType, code } = req.body;

    if (!algorithmType || !code) {
      logger.info("Missing fields in request body");
      return res.status(400).json({
        status: "invalid",
        error: "MISSING_FIELDS",
        message: "Both algorithmType and code are required.",
      });
    }

    const containsAny = (patterns) =>
      patterns.some((pattern) => new RegExp(pattern, 'i').test(code));

    const validators = {
      'Dijkstra': () => {
        // More flexible patterns for Dijkstra
        const requiredPatterns = [
          '\\b(dist(ance)?\\[|\\bdist\\s*=\\s*|\\bmin_dist\\b)', // Distance tracking
          '\\b(heapq|priorityqueue|priority_queue|heappush|heappop|queue)', // Priority queue usage
          '\\b(while|for).*\\b(queue|heap|priority)', // Loop with queue/heap
          '\\b(if\\s+.+\\s*<\\s*dist\\[|dist\\[.+\\]\\s*=\\s*min\\()', // Distance comparison/update
        ];

        const optionalPatterns = [
          '\\bgraph\\b',
          '\\bvisited\\b',
          '\\brelax\\b',
          '\\bneighbor(s)?\\b'
        ];

        logger.info("Validating Dijkstra algorithm...");
        if (!containsAny(requiredPatterns)) {
          logger.info("Dijkstra validation failed");
          return {
            valid: false,
            error: "DIJKSTRA_VALIDATION_FAILED",
            message:
              "Your code misses Dijkstra's key components. Ensure: 1) Priority queue usage, 2) Distance comparison and update, 3) Graph traversal.",
          };
        }
        return { valid: true };
      },

      'Merge Sort': () => {
        const requiredPatterns = [
          '\\b(merge_?sort|mergeSort)\\s*\\(',
          '\\b(merge\\s*\\()|(def\\s+merge\\b)',
          '\\b(left|right)\\s*=\\s*.+\\[.+:.+\\]', // Array splitting
          '\\b(return\\s+merge\\()|(merge\\()' // Merging step
        ];

        logger.info("Validating Merge Sort algorithm...");
        if (!containsAny(requiredPatterns)) {
          logger.info("Merge Sort validation failed");
          return {
            valid: false,
            error: "MERGE_SORT_VALIDATION_FAILED",
            message:
              "Your code misses Merge Sort logic. Ensure: 1) Recursive division, 2) Merging of sorted halves.",
          };
        }
        return { valid: true };
      },

      'Quick Sort': () => {
        const requiredPatterns = [
          '\\b(quick_?sort|quickSort)\\s*\\(',
          '\\b(pivot\\s*=|pivot\\s*=\\s*.+\\[)',
          '\\b(partition\\s*\\()|(def\\s+partition\\b)',
          '\\b(return\\s+quick_?sort\\()' // Recursive calls
        ];

        logger.info("Validating Quick Sort algorithm...");
        if (!containsAny(requiredPatterns)) {
          logger.info("Quick Sort validation failed");
          return {
            valid: false,
            error: "QUICK_SORT_VALIDATION_FAILED",
            message:
              "Your code misses Quick Sort logic. Ensure: 1) Pivot selection, 2) Partitioning logic, 3) Recursive sorting.",
          };
        }
        return { valid: true };
      },

      'BFS': () => {
        const requiredPatterns = [
          '\\b(queue|deque|collections\\.deque)\\b',
          '\\b(while|for)\\s*\\(?.+queue',
          '\\b(visited\\[|visited\\.add\\()',
          '\\b(append|push|enqueue|add)\\s*\\(.+queue',
          '\\b(pop|popleft|dequeue)\\s*\\('
        ];

        logger.info("Validating BFS algorithm...");
        if (!containsAny(requiredPatterns)) {
          logger.info("BFS validation failed");
          return {
            valid: false,
            error: "BFS_VALIDATION_FAILED",
            message:
              "Your code misses BFS logic. Ensure: 1) Queue-based traversal, 2) Visited tracking, 3) Neighbor exploration.",
          };
        }
        return { valid: true };
      },

      'DFS': () => {
        const requiredPatterns = [
          '\\b(dfs\\s*\\()|(def\\s+dfs\\b)',
          '\\b(visited\\[|visited\\.add\\()',
          '\\b(stack\\s*=\\s*\\[)|(recursion)',
          '\\b(pop|append)\\s*\\(',
          '\\b(for\\s+.+\\s+in\\s+.+\\s*:\\s*dfs\\()' // Recursive case
        ];

        logger.info("Validating DFS algorithm...");
        if (!containsAny(requiredPatterns)) {
          logger.info("DFS validation failed");
          return {
            valid: false,
            error: "DFS_VALIDATION_FAILED",
            message:
              "Your code misses DFS logic. Ensure: 1) Stack usage or recursion, 2) Visited tracking, 3) Backtracking.",
          };
        }
        return { valid: true };
      },
    };

    const validatorFn = validators[algorithmType];

    if (!validatorFn) {
      logger.info(`Unknown algorithm type received: ${algorithmType}`);
      return res.status(400).json({
        status: "invalid",
        error: "UNKNOWN_ALGORITHM",
        message: `The algorithm "${algorithmType}" is not supported.`,
      });
    }

    const validation = validatorFn();

    if (!validation.valid) {
      logger.info(`${algorithmType} code validation did not pass.`);
      return res.status(400).json({
        status: "invalid",
        error: validation.error,
        message: validation.message,
      });
    }

    logger.info(`${algorithmType} code validation successful.`);
    return res.status(200).json({
      status: "valid",
      message: `${algorithmType} validation passed.`,
    });
  } catch (error) {
    logger.error("Validation internal error:", error);
    return res.status(500).json({
      status: "error",
      error: "VALIDATION_INTERNAL_ERROR",
      message: "Something went wrong during validation.",
    });
  }
};
const handleGenerateTrace = async (req, res) => {
  try {
    const { code, algorithmName } = req.body;
    console.log("generate trace entered");

    if (!code || !algorithmName) {
      return res.status(400).json({ error: "Both 'code' and 'algorithmName' are required." });
    }

    const sanitizedName = algorithmName.split(' ')[0].toLowerCase();
    const algoTemplate = template[sanitizedName];

    if (!algoTemplate) {
      return res.status(400).json({ error: `No template found for algorithm: ${sanitizedName}` });
    }

    console.log("Sanitized Algorithm:", sanitizedName);
    console.log("User Code:", code);

    // Call Gemini Service to generate trace
    let completeResponse;
    try {
      completeResponse = await GeminiService.generateTrace(code, algoTemplate, algorithmName);
    } catch (geminiError) {
      console.error("Gemini Service Error:", geminiError.message);
      return res.status(500).json({ error: "Failed to generate trace using Gemini" });
    }

    // Save trace to JSON file
    const filePath = path.join(__dirname, `trace.json`);
    try {
      fs.mkdirSync(path.dirname(filePath), { recursive: true });
      fs.writeFileSync(filePath, JSON.stringify(completeResponse, null, 2), 'utf-8');
      console.log("Trace file written successfully");
    } catch (fsError) {
      console.error("File system error:", fsError.message);
      return res.status(500).json({ error: "Failed to write trace file" });
    }

    console.log("Gemini trace completed");
    console.log("Starting bash file");

    // Run bash script
    const scriptPath = "/automate.sh"; // Ensure this is absolute or properly resolved
    exec(`.${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Script execution error: ${error.message}`);
        return res.status(500).json({ message: 'Failed to run script', error: error.message });
      }

      console.log(`Script output: ${stdout}`);
      // Extract HLS_URL from stdout
      const match = stdout.match(/hls URL: (https:\/\/[^\s]+\.m3u8)/);
      console.log(match);
      const hlsUrl = match ? match[1] : null;



     if (!hlsUrl) {
        return res.status(500).json({ message: 'HLS URL not found in script output.' });
      }
      console.log(hlsUrl)
    return res.status(200).json({ message: 'visualization generated successfully.', hlsUrl });
     
    });

  } catch (err) {
    console.error("Unhandled Error:", err.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
};




module.exports = { handleCodeValidation ,handleGenerateTrace};
  