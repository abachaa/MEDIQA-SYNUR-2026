# MEDIQA-SYNUR 2026

**Website:** https://sites.google.com/view/mediqa2026/mediqa-synur

**Codabench:** https://www.codabench.org/competitions/12113/ 


Introduction
-------

This shared task presents the first community challenge centered on nursing data, aimed at advancing methods for clinical documentation. 
The goal is to reduce nursing burden and improve the accuracy and completeness of patient records by automatically capturing clinically salient information from nurse-patient conversations. 
The task focuses on extracting and normalizing clinical observations from conversational transcripts and mapping them to a large ontology of clinical concepts. 


We recently introduced SYNUR, the first dataset designed for observation extraction in nursing dictations. 
Building on this resource, we extend the MEDIQA-OE 2025 shared task to address the unique challenges posed by nurse transcriptions.


For the test phase, participants will be evaluated on a curated and validated benchmark of nurse dictations generated through a controlled multi-agent simulation pipeline. 
Gold-standard annotations were produced by expert nurses using an open-source, large-scale clinical ontology, ensuring high annotation quality and clinical relevance.


Registration
-------

*Step 1:* Please fill out the MEDIQA-SYNUR 2026 registration form at the following link: https://forms.gle/LKeKsuu6iea53mwHA 

If you are unable to access the registration form, please email us at mediqa.organizers@gmail.com with the following information: {first name, last name, team name, affiliation, country/countries of affiliation, codabench username (for run submission), github username (for code submission)}

The registration must be submitted by the team lead or representative (please do not submit multiple registrations from the same team). 

*Step 2:* After submitting the registration form, please review and accept the Terms, and join the Codabench competition using the following link: https://www.codabench.org/competitions/12113/ (You can find the Terms under the Terms page on Codabench). 

Data & Leaderbord
-------

Once your registration form and Codabench access request have been approved, you will be granted access to the dataset on Codabench, as well as the leaderboard where you can submit your runs.

Evaluation
-------

Evaluation script is available at: https://github.com/abachaa/MEDIQA-SYNUR-2026/blob/main/mediqa_synur_eval_script.py 

Example of execution:

    python mediqa_synur_eval_script.py -r ref.jsonl -p pred.jsonl -o output/

Schedule
-------

* First CFP & Registration opens: Mon 8 Dec 2025
* Development data release: Mon 15 Dec 2025
* Registration ends: Fri 30 Jan 2026
* Test data release: Mon 02 Feb 2026
* Run (& code) submission due: Thu 05 Feb 2026
* Release of the results by the organizers: Fri 06 Feb 2026
* Paper submission due: Fri 13 Feb 2026
* Notification of acceptance: Wed 11 Mar 2026
* Final version due: Mon 30 Mar 2026
* ClinicalNLP Workshop: Saturday 16 May 2026, Palma de Mallorca, Spain


Organizers
-------
* Asma Ben Abacha, Microsoft, USA
* Nate Bodenstab, Microsoft, USA
* Jean-Philippe Corbeil, Microsoft, Canada
* George Michalopoulos, Microsoft, Canada 

Contact
-------

If you have any questions regarding your team's registration, please email us at mediqa.organizers@gmail.com

For more updates or inquiries, join the MEDIQA Google group https://groups.google.com/g/mediqa-nlp 
and email us at mediqa-nlp@googlegroups.com (mailing list)

