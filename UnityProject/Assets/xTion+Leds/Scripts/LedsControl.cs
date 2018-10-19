using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using ClientSockets;
using System.Security.Permissions;
using JsonFx.Json;
 
public class LedsControl : MonoBehaviour {
	
	public string ipAddress = "localhost";
	public int portNumber = 30000;
	
	public static LedsControl use = null;
	public SimpleClient ledsClient = new SimpleClient();
	
	private string serverMsg = "Not connected";
	
	void Awake () {
		
		if( use == null ) {
			use = this;
			DontDestroyOnLoad(this.gameObject);
			Debug.Log("LedsControl singleton set to DontDestroyOnLoad");
		}
		else {
			Debug.LogWarning("LedsControl singleton already in scene, auto-destroying");
			Destroy( this );	
		}
		
	}
	
	void Start ()  {
			
		ledsClient.ServerMessage += MessageDecoder;
		Connect();
		
	}
	
	public void Connect() {
		
		bool isConnected = ledsClient.ConnectResult( ipAddress, portNumber );
		if(isConnected) {
			serverMsg = "Connected.";
		}
		else {
			serverMsg = "Connection failed.";
			Debug.LogWarning(serverMsg);	
		}
		
	}
	
	public void SendCommand( string cmd ) {
		
		if(ledsClient.isConnectedToServer()) {
			ledsClient.SendData( cmd );
		}
		else {
			serverMsg = "Not connected to server. Press Enter to connect.";
		}
		
	}
	
	public void SetLedsValue( float intensity ) {	
		SendCommand( "{\"val\":"+intensity+"}" );
	}
	
	public void LerpLedsValue( float intensity , float duration = 1.0f ) {	
		SendCommand( "{\"val\":"+intensity+",\"dur\":"+duration+"}" );
	}
	
	public void GetLedsIntensity() {
		SendCommand( "{\"cmd\":\"get_leds_intensity\"}" );
	}
	
	public void Disconnect() {
		SendCommand( "{\"cmd\":\"disconnect\"}" );
	}
	
	public void Shutdown() {
		SendCommand( "{\"cmd\":\"shutdown\"}" );
	}
	
	public string GetLastServerMessage() {
		return serverMsg;	
	}
	
	void MessageDecoder(string msg) {
		
		Hashtable hash = JsonReader.Deserialize<Hashtable>(msg);
		/*foreach(string key in hash.Keys)
			Debug.Log("key: "+key+"; value: "+hash[key]);*/
		
		serverMsg = "Message from server: "+msg+"\n\n";
		/*
		if(hash.ContainsKey("nbuser")) {
			serverMsg += "Users number : "+hash["nbuser"];
		}
		else if(hash.ContainsKey("users")) {
			AllUsers allUsers = JsonReader.Deserialize<AllUsers>(msg);
			users = allUsers.users;
			
			int nb = users == null ? 0 : users.Length;
			serverMsg += "Deserialized users number: "+nb;
			
			needToRefreshUsers = true;
		}
		else if(hash.ContainsKey("disconnect")) {
			ledsClient.Disconnect();
			serverMsg += "Disconnected from server.";
		}
		else if(hash.ContainsKey("srv_shutdown")) {
			ledsClient.Disconnect();
			serverMsg += "Disconnected from server and server killed.";
		}
		else {
			serverMsg += "Server command not supported.";
		}
		*/
	}
 
	void OnApplicationQuit () {
		
		try
		{
			SetLedsValue( 0 );
			Disconnect();
			ledsClient.ServerMessage -= MessageDecoder;
		}
		catch{}
		
	}
}