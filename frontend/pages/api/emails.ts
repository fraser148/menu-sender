import clientPromise from "../../lib/mongodb";
import type { NextApiRequest, NextApiResponse } from 'next'
import { toIsoString } from "../../lib/dateFormat";

const collection = "emails"

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const client = await clientPromise;
  const db = client.db("exeterMenu");
  switch (req.method) {
    case "POST":
      let bodyObject = JSON.parse(req.body);
      bodyObject.timeStamp = toIsoString(new Date())
      const update = {
        "$set": 
          bodyObject
      };
      const query = { email: bodyObject.email };
      let newEmail = await db.collection(collection).updateOne(query, update, {upsert: true});
      res.json(newEmail);
      break;
    case "GET":
      const posts = await db.collection(collection).find({}).toArray();
      res.json({ status: 200, data: posts });
      break;
  }
}