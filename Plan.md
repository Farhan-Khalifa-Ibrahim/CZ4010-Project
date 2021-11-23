# CZ4010-Project

## Power point
[powerpoint link](https://docs.google.com/presentation/d/12kHPRz6rJX27t0S0U4ka4xq6Q55CTEB-xQll5Plqgp4/edit?usp=sharing)

power point

(Alif)
1. Project apa

2. Ngebedain app kita sama app lain
   - fitur
	what user can do
	- post issue
	- upvote downvote
	- read issue sama redressal
	what admin can do

   - integrity issue -> karena upvote downvote
   - Ada redressal

(Sebastian)
3. kenapa secure 
	- arti secure di app kita -> CIA (confidential,integrity,availability)
	- confidential di db karena user detail di hash ke user_id
	- integrity karena https, 1 email to 1 user

4. Security Firebase
	- jelasin cryptography firebase

5. demo
	- bikin script
         (Alif)
        - user  -> post issue
 		-> upvote downvote issue
		-> liat redressal
		-> upvote downvote redressal
	(Sebastian)
	- Admin -> Liat issue
		-> update issue status (reject,progress,complete)
		-> Redressed issue

## Resource
[Grievance Redressal](https://en.wikipedia.org/wiki/Grievance_redressal)
[Production example app](https://docs.digit.org/)

## Bentuk database
title 1

description 1

addresal 1

title 2

description 2

addresal 2

## Flow terminal
1. Pilih login ato sign up -> pake Firebase Auth, butuh buat sign downvote/upvote/redressal

Sign up
1. Enter username
2. Enter password
3. Balik

Login
1. Enter username
2. Enter password
3. App nentuin user ini user/admin

4. List fitur (user)

	a. liat issue
	
	c. post issue baru

4. list fitur(admin)

	a. post addressal
	
	b. list issue


Pilih list issue
1. Ngelist semua issues -> sort by number of vote, tie breaker time
	1) Bis NTU Lambat (50 👍 3 👎) (IN PROGRESS)
	2) Tugas ini susah banget (26 👍 3 👎) (IN PROGRESS)

2. pilih salah satu issue (misal 1)
3. Display issue detail

Issue Detail
1. title: Bis NTU lambat
   
   desc: Bisnya mepet2, pas dateng selalu full

   category: ADMIN/TRANSPORT/ENVIRONMENT/EDUCATION

   status: PENDING/IN PROGRESS/REDRESSED/REJECTED

   votes: 50 👍 3 👎

   You [have/haven't] voted for this issue

2. Action berdasarkan status
- pending/in progress -> upvote downvote (digital sign pake email user)
- redressed -> view redressal (g ad voting lagi)
- rejected -> N/A (g ad voting lagi)

Liat Redressal
1. List issue (status == IN_PROGRESS/REDRESSED)
2. User pilih issue
3. Display redressal

Issue: Bis NTU lambat
Status: REDRESSED
Redressal id: asjdkasduhid
Votes: 50 👍 3 👎

(4 Nov 2021 07:00) Admin is taking action -> waktu status diganti jd in progress
(4 Nov 2021 08:00) Redirected to supervisor
(4 Nov 2021 10:00) Communicating to Tong Tar Transport
(4 Nov 2021 11:00) Action completed

4. Pilih action berdasarkan status
- in progress -> N/A (g ad action, yg penting user bs liat)
- redressed -> upvote/downvote

pilih post issue baru
1. Pilih category
2. Input title
3. Input desc
3. post ke db

### Admin
2 new issues. (jumlah pending)
3 issues in progress. (jumlah issue in progress)
1 redressal complaint. (jumlah redressal yg banyak downvote)

1. List Issue
2. List Redressed
#### List Issue
1. List semua issue sesuai admin kategori, yg blom redressed, sort sama kek user
2. Pilih issue
3. Display kek user + actionsnya
- Change status -> cmn bs kalo min. ada 10 vote DAN >50% downvote 
- (kalo in progress) Log redressal
- (kalo pending/in progress) Link to another redressal

#### Log Redressal
1. Input redressal message
2. Submit (bareng sama digital signature adminnya)

#### Link to Prev Redressal
1. Input redressal id
2. Submit

#### List Redressed
1. List issue yg udh redressed, tp pake redressal pov, sort pake jumlah vote, tp klo jumlah vote > 10 dan persentase downvote > 70% jd priority
	1) Redressal for "Bis NTU Lambat" (3 👍 49 👎)
	2) Redressal for "Tugas susah" (17 👍 3 👎)
2. Pilih issue
3. Action: re-redress (statusnya balik jd in progress)

Considerations
1.	Someone posts a grievance, but it is not a valid one. Thus, unfair to the accused.
a.	There may be a voting mechanism where others “sign” the same petition. (jumlah sama proporsi vote nentuin ini beneran apa engga)
b.	There must be a checks-and-balances mechanism to stop “false” claims. (admin bisa reject kalo vote cukup banyak(10) AND >70% downvote)
2.	Someone posts a grievance, but it is not redressed. This is unfair to the accuser.
a.	There may be an acknowledgement seeking mechanism from the accused. (post issue, trus divote orang2 publik)
b.	There must be a way to “limelight” the grievances which are not redressed. (issue yg paling banyak divote bakal muncul di awal)
3.	Someone posts a grievance, it is redressed, but nobody knows about the case.
a.	Every redressed grievance should have a proper documentation trail record. (user bs liat redressal timeline)
b.	Once again, there may be a voting mechanism for others to confirm this case. (abis redressed, user bs vote. kalo downvote banyak admin dinotify)
 
