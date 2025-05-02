import React from 'react'

import { hlsURL, secureURL } from "../../utils/utils"
const VideoPlayer = ({videoRef}) => {
  return (
    <div>
      <div className="mt-6 space-y-4">
          <h3 className="text-xl font-semibold">Generated Visualization</h3>

          <video
            ref={videoRef}
            className="video-js vjs-default-skin"
            controls
            preload="auto"
            width="640"
            height="360"
          >
            <source src={hlsURL} type="application/x-mpegURL" />
          </video>

          {/* <video src={secureURL} controls width="640" height="360" className="border rounded-md shadow" /> */}
        </div>
    </div>
  )
}

export default VideoPlayer
