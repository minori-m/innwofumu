using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class ReceiveText : MonoBehaviour {
	public PythonReceiver_Flask01 Receiver_Flask01;
	// Use this for initialization
	void Start () {
	}
	
	// Update is called once per frame
	void Update () {
		if(Receiver_Flask01.PythonString != null)
		{
			GetComponent<TextMeshPro>().text = Receiver_Flask01.PythonString;
		}
	}
}
