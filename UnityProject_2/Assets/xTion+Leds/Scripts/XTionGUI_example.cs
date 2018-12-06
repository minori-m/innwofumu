using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class XTionGUI_example : MonoBehaviour {
	
	public GUIText numberText;
	public GameObject userGO;
	
	private List<GameObject> usersGO = new List<GameObject>();
	private KinUser[] users;
	
	void Update () {
		
		if (Input.GetKeyDown (KeyCode.Return)) {
			XTionControl.use.Connect();
		}
		else if (Input.GetKeyDown (KeyCode.Space)) {
			XTionControl.use.GetUserNumber();
		}
		else if (Input.GetKeyDown ("u")) {
			XTionControl.use.GetUsers();
		}
		else if (Input.GetKeyDown ("q")) {
			XTionControl.use.Disconnect();
		}
		else if (Input.GetKeyDown ("s")) {
			if(XTionControl.use.xtionClient.isConnectedToServer()) {
				XTionControl.use.Shutdown();
			}
		}
		
		numberText.text = XTionControl.use.GetLastServerMessage();
		
	}
	
	void OnConnected( bool isConnected ) {
		Debug.Log("OnConnected: " + isConnected );
	}
	
	void OnUserNumber( int number ) {
		Debug.Log("OnUserNumber: " + number );
	}
	
	void OnUsers( KinUser[] users ) {
		Debug.Log("OnUsers: " + users.Length );
		this.users = users;
		RefreshUsersGO();
	}
	
	void RefreshUsersGO() {
		
		if(users == null || users.Length <= 0) {
			foreach(GameObject go in usersGO)
				GameObject.Destroy(go);
			usersGO = new List<GameObject>();	
		}
		else {
			
			List<GameObject> list = new List<GameObject>();
			
			// remove user no more in the scene
			foreach(GameObject go in usersGO) {
				UserGO script = go.GetComponent<UserGO>();
				bool found = false;
				
				foreach(KinUser ku in users) {
					if(script.CompareUser(ku)) {
						list.Add(go);
						found = true;
						break;
					}
				}
				if(!found)
					GameObject.Destroy(go);
			}
			
			// update existing users and add new users.
			foreach(KinUser ku in users) {
				
				bool isNewUser = true;
				
				foreach(GameObject go in list) {
					UserGO script = go.GetComponent<UserGO>();
					if(script.CompareUser(ku)) {
						script.UpdatePosition(ku);
						isNewUser = false;
						break;
					}
				}
				
				if(isNewUser) {
					GameObject newGO = GameObject.Instantiate(userGO) as GameObject;
					UserGO script = newGO.GetComponent<UserGO>();
					script.User = ku;
					list.Add(newGO);	
				}
				
			}
			
			usersGO = list;
			
		}
				
	}
}
