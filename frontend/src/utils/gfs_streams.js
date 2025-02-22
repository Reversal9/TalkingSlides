const mongoose = require("mongoose");
const Grid = require("gridfs-stream");
const fs = require("fs");

const conn = mongoose.createConnection("mongodb://localhost:27017/videosDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

let gfs;
conn.once("open", () => {
  gfs = Grid(conn.db, mongoose.mongo);
  gfs.collection("uploads");
});

// Upload a video
const uploadVideo = (filePath, filename) => {
  const writestream = gfs.createWriteStream({ filename });
  fs.createReadStream(filePath).pipe(writestream);
};
