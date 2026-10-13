# Fact-check B (2026-10-12)

Scope: D&C 93, 98, 101, 103, 107, 109, 110, 111, 115, 119, 121, 124, 127, 128, 130, 131, 132, 134, 135, 136, 137, 138, OD1, OD2.
Method: I read the full verse text for each section and checked the official heading for every item. I also read the JSP historical introduction for 93, 98, 101, 103, 115, 132 and 134. I checked each ldsText lesson against cfm-2025.json, and checked the ODs against the live 2025 manual. I ran check_section.py on every numbered file. All pass with no errors or warnings.

Result: 12 of 24 items needed a fix. 9 of those were substantive errors. The other 3 were omissions or overreach.

| Item | Result |
|---|---|
| 93 | FIXED. The setting said the "Bible revision" was finished in February. The JSP says the New Testament revision was finished on 2 February 1833. The summary said Joseph and Williams were sent to "travel and preach", but v. 52 only says "make haste also". Corrected. |
| 98 | FIXED (minor). The summary left out vv. 41–45, which say to forgive an unrepentant enemy three times and then bring testimonies before the Lord. Added. The contextNote added "in every setting" to v. 16, which the text does not say. Removed. |
| 101 | FIXED. The summary called vv. 23–34 "the Millennium", a term the text does not use. It also stopped the parable halfway and left out the redemption of the vineyard (vv. 55–62). Both corrected. Setting facts confirmed by JSP: Hyde and Gould arrived 25 Nov, letters arrived 10 Dec, the "be still" letter, Ames's account. |
| 103 | OK. The JSP confirms "thirty or forty" volunteers and that the order of the revelation and the meeting is uncertain. |
| 107 | OK. The heading confirms vv. 60–100 come largely from November 1831 and that the section is tied to the Twelve and the 4 May 1835 departure. |
| 109 | OK |
| 110 | OK |
| 111 | OK |
| 115 | OK. The JSP confirms the July 1837 excavation, the pause in November 1837, the March 1838 move, and Robinson's copy. |
| 119 | OK |
| 121 | OK. Minor note, not changed: emma-smith is in personIds only because the letters were sent to her. She is not named in the text. |
| 124 | OK. "Madison" (v. 88) as Fort Madison is still unverified, as the writer noted. |
| 127 | OK |
| 128 | OK |
| 130 | OK |
| 131 | OK |
| 132 | FIXED. The last summary sentence ("if she rejects it, he is exempt") was vague. It left out v. 64's warning that a wife who rejects the law "shall be destroyed". It also did not say what he is exempt from ("the law of Sarah", her consent). Rewritten to state vv. 61–65 accurately. The Emma sentences were merged to keep the sentence count. The setting was checked against the JSP: about 25 sealings, most of the 1843 sealings made without Emma's knowledge, Hyrum's request, Emma burning the original, Kingsbury's copy, 1852 and 1876. All accurate. |
| 134 | FIXED (balance). The setting gave no context for v. 12 on enslaved people. Added the JSP note that it answered Missouri charges of abolitionism. Merged two setting sentences to stay within length. |
| 135 | FIXED. The summary said the brothers' blood is "a witness against Illinois". V. 7 calls it "a witness to the truth of the everlasting gospel", and names Illinois for its broken pledge. The contextNote's "stand charged" wording for v. 7 was reworded to match. |
| 136 | OK. Minor, not changed: people named in vv. 12–14 (Benson, Snow, Lyman, G. A. Smith) are not in people-ids. |
| 137 | OK |
| 138 | FIXED. The summary implied Joseph and Hyrum Smith were among the messengers Christ organized. Vv. 53–56 instead place them in the spirit world as spirits reserved for the latter days. Corrected. |
| OD1 | FIXED. The ldsText did not name a Come, Follow Me lesson. cfm-2025.json has no entry for the ODs. The real lesson, checked on the live manual, is 8–14 December, "We Believe": Articles of Faith and Official Declarations 1 and 2. Added. The facts were checked against the OD1 page and are accurate. |
| OD2 | FIXED. The ldsText did not name the lesson. Added. The summary left out that the letter extends temple blessings, even though the title promises them. Added. The setting said "later leaders" imposed the temple restriction, but it began under Brigham Young as well. Reworded. The 1852 Brigham Young detail is from the Gospel Topics essay, not the OD2 heading. It is accurate, but the setting does not cite it. |

## Notes for the project
- cfm-2025.json is missing the 8–14 December lesson that covers OD1 and OD2. Add it.
- od1.json and od2.json use a smaller schema: no contextNote content, sources, or reviewNote, and check_section.py cannot check them. I added a reviewNote field to each. They were checked by hand for sentence length and banned words.
