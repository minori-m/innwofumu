using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;  ////ここを追加////
using System.IO;

public class GetText : MonoBehaviour {
    //通信開始（http://localhost:5000/）
    public string[] PythonStrings = new string[10];
    public string PythonString = "";
    public void connectionStart(string name)
    {
        string POST_URL = "http://localhost:5000/";
        WWW www = new WWW(POST_URL);
        StartCoroutine("WaitForRequest", www);
    }
    //通信の処理待ち
    private IEnumerator WaitForRequest(WWW www)
    {
        yield return www;
        connectionEnd(www);
    }
    //通信終了後の処理
    private void connectionEnd(WWW www)
    {
        //通信結果をLogで出す
        if (www.error != null)
        {
            Debug.Log(www.error);
            // var strB = www.error.Substring(0,11);
            var strB = www.text;
            GetComponent<Text>().text = strB;
            textSave(strB);
        }
        else
        {
            //通信結果 -> www.text
            Debug.Log(www.text);
            // var strA = www.text.Substring(0,11);
			var strA = www.text;
            PythonString = strA;
            PythonStrings = splitPythonList(strA);

            GetComponent<Text>().text = strA;
            textSave(strA);
        }
    }
    // Update is called once per frame
    void Update()
    {
        connectionStart(name);
    }
    // 引数でStringを渡してやる
    public void textSave(string txt)
    {
        StreamWriter sw = new StreamWriter("LogData.txt", false); //true=追記 false=上書き
        sw.WriteLine(txt);
        sw.Flush();
        sw.Close();
    }

    public string[] splitPythonList(string str)
	{
		string strClean = str.Replace("[","").Replace("]","");
		string[] strS = new string[10];
		strS = strClean.Split(',');
		return strS;
	}
}