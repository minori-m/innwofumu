using UnityEngine;
using System.Collections;

public class LedsGUI_example : MonoBehaviour {
	
	public GUIText numberText;
	
	void Update () {
		
		if (Input.GetKeyDown (KeyCode.Return)) {
			LedsControl.use.Connect();
		}
		else if (Input.GetKeyDown (KeyCode.Space)) {  // get the current intensity of the leds
			LedsControl.use.GetLedsIntensity();
		}
		else if (Input.GetKeyDown ("o")) { // turn leds on
			LedsControl.use.LerpLedsValue( 1.0f, 1 );
		}
		else if (Input.GetKeyDown ("p")) { // turn leds off
			LedsControl.use.LerpLedsValue( 0.0f, 1 );
		}
		else if (Input.GetKeyDown ("r")) { // turn leds at rnd value
			LedsControl.use.LerpLedsValue( Random.Range( 0.0f, 1.0f ) , Random.Range( 0.5f, 1.0f ) );
		}
		else if (Input.GetKeyDown ("m")) { // set leds at middile intensity
			LedsControl.use.SetLedsValue( 0.5f );
		}
		else if (Input.GetKeyDown ("q")) { // set leds at middile intensity
			LedsControl.use.Disconnect();
		}
		
		numberText.text = LedsControl.use.GetLastServerMessage();
		
	}
}
