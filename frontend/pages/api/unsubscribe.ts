import clientPromise from "../../lib/mongodb";
import type { NextApiRequest, NextApiResponse } from 'next'
import { toIsoString } from "../../lib/dateFormat";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const client = await clientPromise;
  const db = client.db("exeterMenu");
  switch (req.method) {
    case "POST":
      let bodyObject = JSON.parse(req.body);
      bodyObject.timeStamp = toIsoString(new Date())
      const query = { email: bodyObject.email };
      let unsub = await db.collection("emails").deleteOne(query)
      if (unsub.deletedCount > 0) {
        await db.collection("unsub").insertOne(bodyObject);
      }
      res.json(unsub);
      break;
  }
}