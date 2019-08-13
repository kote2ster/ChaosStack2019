using System;
using System.Net;
using System.Text;
using Newtonsoft.Json;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;
using System.IO;

/*
{
  "userCommands": [
    {
      "user": "Tamara Murphy",
      "action": "on",
      "targetRoom": "utility room"
    },
    {
      "user": "Walter Murphy",
      "action": "on",
      "targetRoom": "dining room"
    },
    {
      "user": "Chris Griffith",
      "action": "on",
      "targetRoom": "utility room"
    },
    {
      "user": "Timothy Morris",
      "action": "on",
      "targetRoom": "guest room"
    },
    {
      "user": "Jeffrey Tate",
      "action": "on",
      "targetRoom": "utility room"
    },
    {
      "user": "Michael Lam",
      "action": "on",
      "targetRoom": "utility room"
    },
    {
      "user": "Adrienne Nelson",
      "action": "on",
      "targetRoom": "attic"
    },
    {
      "user": "Jason Anderson",
      "action": "on",
      "targetRoom": "porch"
    },
    {
 */
namespace ChaosStack2019Autumn
{
    class Program
    {
        static string token = "72d8a515fa01adbdcf874b058149c3d5c337a53353d607cb338136748f82c128";
        static void Main()
        {
            byte[] data = new WebClient().DownloadData("https://chaosstack-xu1aet.s3.eu-central-1.amazonaws.com/mapping.json");
            var jsonstring = Encoding.UTF8.GetString(data);
            var usermap = JObject.Parse("{ \"data\":" + jsonstring + "}")["data"];
            var commands = JObject.Parse(GetCommands());
            foreach (var elem in commands["userCommands"] as JArray)
            {
                //Console.WriteLine("Processing " + elem["user"] + "[" + elem["targetRoom"] + "]: " + elem["action"] + " ...");
                Console.WriteLine("Processing " + elem["user"] + " ...");
                foreach (var user in usermap)
                {
                    if(user["user"].ToString() == elem["user"].ToString())
                    {
                        if(user["rooms"][elem["targetRoom"].ToString()] != null)
                        {
                            Console.WriteLine("\t" + elem["targetRoom"] + ":" + ((JArray)user["rooms"][elem["targetRoom"].ToString()]).Aggregate("",(c,n) => c += " " + n));
                            SetLights(elem["action"].ToString(), ((JArray)user["rooms"][elem["targetRoom"].ToString()]).Select(x => x.ToString()).ToList());
                        }
                    }
                }
            }
            Console.WriteLine("-- DONE --");
        }

        public static string GetCommands()
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create("https://registration.hungary.chaosstack.com/api/qualify/user_commands");
            request.AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate;
            request.Headers.Add("Authorization", token);
            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using (Stream stream = response.GetResponseStream())
            using (StreamReader reader = new StreamReader(stream))
            {
                return reader.ReadToEnd();
            }
        }

        public static string SetLights(string state, List<string> ids)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create("https://registration.hungary.chaosstack.com/api/qualify/set_lights");
            request.AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate;
            request.Method = "POST";
            request.ContentType = "application/json";
            request.Headers.Add("Authorization", token);
            var j = new JObject();
            j.Add("desiredState", state);
            j.Add("lights", new JArray(ids));
            byte[] json = Encoding.ASCII.GetBytes(JsonConvert.SerializeObject(j));
            request.GetRequestStream().Write(json, 0 , json.Length);
            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using (Stream stream = response.GetResponseStream())
            using (StreamReader reader = new StreamReader(stream))
            {
                return reader.ReadToEnd();
            }
        }
    }
}
