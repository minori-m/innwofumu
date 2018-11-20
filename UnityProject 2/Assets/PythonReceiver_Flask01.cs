using System;
using System.Text.RegularExpressions;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PythonReceiver_Flask01 : MonoBehaviour {
	public string PythonString = "";
	public List<string> PythonList = new List<string>();
	string pythonStringClean = "";
	public string[] PythonStrings = new string[10];

	IEnumerator Start()
	{
		WWW www = new WWW("http://localhost:5000/");

		yield return www;
		// www.text contains string array that is converted into one string, so we need to separate them manually.
		Debug.Log(www.text);
		pythonStringClean = www.text.Replace("[","").Replace("]","");
		PythonStrings = pythonStringClean.Split(',');
		//PythonString = www.text;

		for(int i = 0; i < PythonStrings.Length; i++)
		{
			Debug.Log(PythonStrings[i]);
		}
	}
	public void Update()
	{
		// WWW www = new WWW("http://localhost:5000/");

		// yield return www;
		// // www.text contains string array that is converted into one string, so we need to separate them manually.
		// Debug.Log(www.text);
		// pythonStringClean = www.text.Replace("[","").Replace("]","");
		// PythonStrings = pythonStringClean.Split(',');
		Debug.Log("Update");
	}

	public string[] splitPythonList(string str)
	{
		string strClean = str.Replace("[","").Replace("]","");
		string[] strS = new string[10];
		strS = strClean.Split(',');
		return strS;
	}
}