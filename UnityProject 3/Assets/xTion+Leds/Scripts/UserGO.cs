using UnityEngine;
using System.Collections;

public class UserGO : MonoBehaviour {
	
	KinUser user;
	
	public KinUser User {
		get { return user; }
		set {
			user = value;
			transform.localPosition = new Vector3(value.x-0.5f, value.y-0.5f, value.dist); 
			TextMesh script = GetComponentInChildren<TextMesh>();
			script.text = "" + value.id;
		}
	}
	
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}
	
	public void UpdatePosition(KinUser user) {
		this.user = user;
		transform.localPosition = new Vector3(user.x-0.5f, user.y-0.5f, user.dist); //*Camera.main.fieldOfView; 	
	}
	
	public bool CompareUser(KinUser user) {
		return this.user.id == user.id;
	}
	
}
