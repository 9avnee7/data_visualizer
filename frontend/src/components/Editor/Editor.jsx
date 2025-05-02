import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import VideoPlayer from './videoPlayer/videoPlayer';

const Editor = () => {
  const [algorithm, setAlgorithm] = useState('');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [videoReady, setVideoReady] = useState(false);
  const videoRef = useRef(null);
  const playerRef = useRef(null); 

  const algorithms = ['Dijkstra', 'Merge Sort', 'Quick Sort', 'BFS', 'DFS'];

  useEffect(() => {
    if (videoReady && videoRef.current && !playerRef.current) {
      playerRef.current = videojs(videoRef.current, {
        autoplay: true,
        controls: true,
        preload: 'auto',
        fluid: true,
      });
    }

    return () => {
      if (playerRef.current) {
        playerRef.current.dispose();
        playerRef.current = null;
      }
    };
  }, [videoReady]); // re-run when video becomes ready

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setVideoReady(false); // Reset video

    try {
      // Step 1: Validate
      const res = await axios.post('http://localhost:3000/api/validate', {
        algorithmType: algorithm,
        code,
      });
      console.log(res)
      alert(res.data.message);

      // Step 2: Generate trace (but don't expect HLS from response)
      await axios.post(
        'http://localhost:3000/api/trace',
        {
          algorithmName: String(algorithm),
          code: String(code),
        },
        {
          headers: { 'Content-Type': 'application/json' },
        }
      );

      // Step 3: Assume the trace and video are generated and available at known HLS URL
      setVideoReady(true);
      

    } catch (err) {
      alert(err.response?.data?.message || 'An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-semibold mb-4">Real-Time Algorithm Visualizer</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium">Select Algorithm</label>
          <select
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            required
          >
            <option value="">-- Choose an algorithm --</option>
            {algorithms.map((algo) => (
              <option key={algo} value={algo}>
                {algo}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block font-medium">Paste Python Code</label>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows="10"
            className="w-full border border-gray-300 rounded-md p-2 font-mono"
            placeholder="Paste your Python implementation here"
            required
          ></textarea>
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Visualize'}
        </button>
      </form>

      {videoReady && (
        <VideoPlayer videoRef={videoRef}/>
      )}
    </div>
  );
};

export default Editor;
