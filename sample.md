We have an enterprise tool called X. This tool is primarily used by an investment bank to To make regulatory attestations on a yearly or biennial basis. In terms of the users, it has certain types of users:
the department owner
the admin, which is the product admin, which is X's admin
Executor and the 
next one, a Challenger
All of them have certain tasks and a certain time-bounded way of executing them. In short, the flow is like this at a very high level:
The admin really takes any particular, let's say, regulatory document and breaks it down into articles. Let's say one particular regulatory document can have three articles.
These articles have certain things that the executor has to conform to and also provide evidence for. The challenger can challenge the executor's working and also add anything on top of that.
The owner can read through both the executor's and the challenger's documents and finally approve.
This makes the article confirmed.
This is generally used either to be shared with the regulator or kept for an internal audit point of view. The challenger, executor, and owner are this set list of people that the admin manages and controls.
Now, the admin's job, if I get into the details, will be like this. They would keep a master record, and let's say, for the time being, tabular-formatted data where there will be:
an article number from where the article is coming from
the master article's name
the actual description of the article
the owner who should be finally approving it
the executor
the challenger
Every article has three sets of challenges, which are optional in nature:
regulatory challenger
process challenger
operational challenger
Three names. I will let you know more in detail and in depth about the three names, and these are optional.

The admin has full control when it is releasing an article for an evidence-gathering exercise, and when the workflow is started, it can choose who would be the executor and who would be the challenger. You do not always need three challenges; you can also have one challenger in one case. In some cases of the article, that's an option that you want to provide.

The admin will be able to monitor the entire workflow. They will be able to see the entire workflow when the workflow is getting created. They will be able to change who is part of it:
an executor
a challenger
an owner
They would be the owner of the product in this case when it comes to the executor. When an article is released, they see that in a tray and get to act on it. They get to see how they should conform to it and provide evidence for it. They write comments and have various fields that they can fill in.

Since every year there is a fixed set of articles, and every year is more like updating the evidence and all at the backend, the admin team has done that. They have mapped the last year's or the prior year's article IDs, which are defined as per the nomenclature of the admin, with the new article ID.

The way they do it right now, and something that we need to solve for, is that they do concatenate over the entire row of the article:
article code
the article number
the article's description
the article's main body's name
If it matches with the newer one, that's how the lineage is drawn. It also opens up a problem: in case there is any change, even a certain bit, there is no lineage connection that we can build. This is something that the admins want to solve for because it eases the process if you know the lineage.

For example, let's say one article is similar to and exactly the same as a prior year's article. You would want to know if you can use evidence from prior, and it would simplify the writing for executives and challengers. In a flow, if that is solved, that would be great.

For an executor, right now, if the mapping is done correctly and if they are able to see older data, they can just use the older data as filings and, of course, take direct input or map it straight to the current article's attestations.

Once the attestation is approved from the executor side, we have a parallel flow where it goes to three different challenges at max. Each challenger, by themselves, can see what the executor has written and also see in real time what the other two challenges have written. In case there is just one challenger, they will be just seeing their own, and others will be disabled. They have the ability to send it back to an executor queue or modify and further enhance the data schema of the article (in terms of, let's say, they can add more documents, more content, and context and all those things).

We do have to clarify what happens if any of the challengers, when there are more than one challenger, sends it back to the executor queue. What happens to the other two challengers' queues? Do they also get sent back? Does it get disabled, or are they independently allowed to keep on modifying? That's something that we have to figure out.

Let's say it goes from the challengers' side and all the challengers approve of it and add whatever necessary information they want to add. Basically, the data schema of that article row is now much more enhanced, and it now goes to an owner strip where an owner can verify and vet and do the final attestation on the same.
