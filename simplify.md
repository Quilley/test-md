# Simplify

I think it's time to reflect back and it's time to just focus on the essentials especially when it comes to TUI. I think we have overdone it when it comes to the UI and there are a lot of elements which seem unnecessary and are also complicating the entire experience when we are developing it.

The core thing that we have to do is that from the TUI you should be able to run the cases and get the status of those run cases. It would record the outputs from the runs and, alongside them, the other metadata that it is supposed to be recording. It is supposed to store them in a .csv. Of course it's also going to collect some other data.

In the journey when it comes to the TUI, I think let's just simplify it to just one option right now in the home button. The one option is the journey that we would follow: the moment you click on "Turnstile: Test" or "Run Tests," you would go to the next screen. It will show you a summary of all the test cases that are available and you get to select which model. You select the model, which will basically change the run.json's model name. You would maybe be able to select repeats just for you to be more sure. Maybe you can explore a little bit if you want to add those repeat features or not but the model seems to be one important aspect.

Once you select the model you will be able to verify. Once you verify you get another screen. It will show you the estimated cost of the run, the estimated runtime, the cases that it will run, and where it will store the final copy, the .dotcsb that is human-verifiable.

Once you verify and start running, it will show you the associated UI. Maybe we will just give a button for you to go back to the home but that will still keep the thing running. The test keeps running as long as Janus TUI is open. We can either pause or save it. We have those features.

That's it. That's how simplified I want things to be because for me it's more important to know that this set of Turnstile tests is being recorded and for what. As they are being recorded I want the journey also to be smooth for the testers and for us to be logging the right things in the right manner in .csv. That's more important to us. We can of course create various variations of it and all those things going forward and those things will be added on the TY page. That is something that we will take up in the next phase.

It's important that we lock down these things and simplify the flow so that we can take each of the journeys more minutely and more critically rather than building it all at once. What you may now be going through is a redaction. In this redacted journey I want you to take various steps: if we have some things that we have done well but we may not need them right now, we keep them aside. Focus more on correctly implementing one feature and the associated flow very well, which is very crucial to us.

What I'm thinking is that we create another subfolder called Janus_TUI_2, which takes elements from Janus_TUI rather than disturbing what we have in Janus_TUI. It takes the right elements out of it and builds it right.

Something that I missed saying is that you have to understand that while we are testing it, we also do call up fixtures, do sweeps, and all those things. Just be mindful of that when we are building this Janus_TUI_2 because it's going to invoke these from the main Janus.
