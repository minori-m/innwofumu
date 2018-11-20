using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using ClientSockets;
using System.Security.Permissions;
using JsonFx.Json;
 
public class XTionControl : MonoBehaviour {
	
	public string ipAddress = "localhost";
	public int portNumber = 33000;
	
	public string connectionCB = "OnConnected";
	public string userNumberCB = "OnUserNumber";
	public string usersCB = "OnUsers";
	public GameObject receiverGO;
	
	public static XTionControl use = null;
	public SimpleClient xtionClient = new SimpleClient();
	
	private string serverMsg = "Not connected";
	
	private int nbUser = 0;
	private KinUser[] kinUsers = null;
	
	private bool sendUserNumberCB = false;
	private bool sendUsersCB = false;
	
	void Awake () {
		
		if( use == null ) {
			use = this;
			DontDestroyOnLoad(this.gameObject);
			Debug.Log("XTionControl singleton set to DontDestroyOnLoad");
		}
		else {
			Debug.LogWarning("XTionControl singleton already in scene, auto-destroying");
			Destroy( this );	
		}
		
	}
	
	void Start ()  {
		
		//needToRefreshUsers = false;
			
		xtionClient.ServerMessage += MessageDecoder;
		Connect();
		
	}
	
	void Update() {
		
		if( sendUserNumberCB ) {
			if( receiverGO != null )
				receiverGO.SendMessage( userNumberCB, nbUser, SendMessageOptions.DontRequireReceiver );
			sendUserNumberCB = false;
		}
		
		if( sendUsersCB ) {
			if( receiverGO != null )
				receiverGO.SendMessage( usersCB, kinUsers, SendMessageOptions.DontRequireReceiver );
			sendUsersCB = false;
		}
		
	}
	
	public string GetLastServerMessage() {
		return serverMsg;	
	}
	
	public void Connect() {
		
		bool isConnected = xtionClient.ConnectResult( ipAddress, portNumber );
		if(isConnected) {
			serverMsg = "Connected.";
		}
		else {
			serverMsg = "Connection failed.";
			Debug.LogWarning(serverMsg);	
		}
		if( receiverGO != null )
			receiverGO.SendMessage( connectionCB, isConnected, SendMessageOptions.DontRequireReceiver );
		
	}
	
	public void SendCommand(string cmd) {
		
		if(xtionClient.isConnectedToServer()) {
			xtionClient.SendData("{\"cmd\":\""+cmd+"\"}");
		}
		else {
			serverMsg = "Not connected to server. Press Enter to connect.";
		}
		
	}
	
	public void GetUserNumber() {
		SendCommand("nbuser");
	}
	
	public void GetUsers() {
		SendCommand("users");
	}
	
	public void Disconnect() {
		SendCommand("disconnect");
	}
	
	public void Shutdown() {
		SendCommand("srv_shutdown");
	}
	
	void MessageDecoder(string msg) {
		
		Hashtable hash = JsonReader.Deserialize<Hashtable>(msg);
		
		serverMsg = "Message from server: "+msg+"\n\n";
		
		if(hash.ContainsKey("nbuser")) {
			int.TryParse( hash["nbuser"].ToString(), out nbUser);
			serverMsg += "Users number : "+nbUser;
			sendUserNumberCB = true;
		}
		else if(hash.ContainsKey("users")) {
			AllUsers allUsers = JsonReader.Deserialize<AllUsers>(msg);
			kinUsers = allUsers.users;
			sendUsersCB = true;
			
			int nbUser = kinUsers == null ? 0 : kinUsers.Length;
			serverMsg += "Deserialized users number: "+nbUser;
		}
		else if(hash.ContainsKey("disconnect")) {
			xtionClient.Disconnect();
			serverMsg += "Disconnected from server.";
		}
		else if(hash.ContainsKey("srv_shutdown")) {
			xtionClient.Disconnect();
			serverMsg += "Disconnected from server and server killed.";
		}
		else {
			serverMsg += "Server command not supported.";
		}
		//Debug.Log( serverMsg );
		
	}
 
	void OnApplicationQuit () {
		
		try
		{
			SendCommand("disconnect");
			xtionClient.ServerMessage -= MessageDecoder;
		}
		catch{}
		
	}
}