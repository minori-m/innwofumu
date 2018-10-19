using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PythonReceiver_Flask01 : MonoBehaviour {
	public string PythonString = "";

	IEnumerator Start()
	{
		WWW www = new WWW("http://localhost:5000/");

		yield return www;
		PythonString = www.text;

		Debug.Log(www.text); //Hello
	}
}
