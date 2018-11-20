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
		// Receiver_Flask01.Update();
		if(Receiver_Flask01.PythonString != null)
		{
			
			for(int i = 0; i < transform.childCount; i++)
        	{
				// Debug.Log("child " + i);
            	//transform.GetChild(i).gameObject.GetComponent<TextMeshPro>().text = Receiver_Flask01.PythonList[i];
				Debug.Log(Receiver_Flask01.PythonStrings[i]);
				transform.GetChild(i).gameObject.GetComponent<TextMeshPro>().text = Receiver_Flask01.PythonStrings[i];
        	}
					// GetComponent<TextMeshPro>().text = Receiver_Flask01.PythonString;
		}
	}
}
