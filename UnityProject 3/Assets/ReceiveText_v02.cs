using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
public class ReceiveText_v02 : MonoBehaviour {
	public GetText Receiver_Flask02;
	// Use this for initialization
	string prevString = "";
	string[] rhymeTexts = new string[9];
	string emptyStringArr = ",,,,,,,,";
	public Sprite Square;
	public Sprite Oval;
	void Start () {
		Debug.Log(transform.GetChild(0).childCount);
		for(int i = 0; i < rhymeTexts.Length; i++)
		{
			rhymeTexts[i] = "";
		}
	}
	
	// Update is called once per frame
	void Update () {
		if(Receiver_Flask02.PythonString != null || Receiver_Flask02.PythonString != emptyStringArr)
		{
			if(Receiver_Flask02.PythonString != prevString)
			{
				for(int i = 0; i < transform.GetChild(0).childCount; i++)
					{
						// Debug.Log("child " + i);
						// Debug.Log(Receiver_Flask02.PythonStrings[i]);

						// Texts Appear
						if(rhymeTexts[i] == "" && Receiver_Flask02.PythonStrings[i] != "")
						{
							transform.GetChild(0).GetChild(i).gameObject.GetComponent<Image>().sprite = Square;
							transform.GetChild(0).GetChild(i).gameObject.GetComponent<Animator>().SetInteger("State",2);
						}
						//Texts Change
						if(rhymeTexts[i] != "" && rhymeTexts[i] != Receiver_Flask02.PythonStrings[i])
						{
							transform.GetChild(0).GetChild(i).gameObject.GetComponent<Animator>().SetInteger("State",3);
						}
						//Texts Disappear
						if(rhymeTexts[i] != "" && Receiver_Flask02.PythonStrings[i] == "")
						{
							transform.GetChild(0).GetChild(i).gameObject.GetComponent<Image>().sprite = Square;
							transform.GetChild(0).GetChild(i).gameObject.GetComponent<Animator>().SetInteger("State",4);
						}


						//Latter
						rhymeTexts[i] = Receiver_Flask02.PythonStrings[i];
						transform.GetChild(0).GetChild(i).GetChild(0).gameObject.GetComponent<TextMeshProUGUI>().text = Receiver_Flask02.PythonStrings[i];
						
					}
			}
			prevString = Receiver_Flask02.PythonString;
		}
	}

	public string[] splitPythonList(string str)
	{
		string strClean = str.Replace("[","").Replace("]","");
		string[] strS = new string[10];
		strS = strClean.Split(',');
		return strS;
	}
}