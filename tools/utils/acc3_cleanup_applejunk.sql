BEGIN TRANSACTION;

-- REMOVE METADATA (and more) from applecoredata

DELETE FROM ZACCOUNTTYPE
WHERE Z_PK IN (
  SELECT ZACCOUNTTYPE FROM ZACCOUNT WHERE ZPARENTACCOUNT IS NOT NULL 
)
AND Z_PK NOT IN ( -- i dont know if i'll need this or not but its safer and wont affect anything
  SELECT ZACCOUNTTYPE FROM ZACCOUNT WHERE ZPARENTACCOUNT IS NULL 
);

-- deleting child accounts property rows within ZACCOUNTPROPERTY
DELETE FROM ZACCOUNTPROPERTY
WHERE ZOWNER IN (
  SELECT Z_PK FROM ZACCOUNT WHERE ZPARENTACCOUNT IS NOT NULL 
)
-- DO NOT fix the typos, or else they will get identified in a later string match
OR ZKEY IN( 
  'DAAccountUseTrustedSSLCertificate',
  'DAAccountPort',
  'DAAccountHost',
  'DAAccountPrincipalPath',
  'DAAccountDidAutodiscover',
  'DAAccountUseSSL',
  'account-exists',
  'UsesCloudDocs',
  'cloudDocsMigrationComplete',
  'protocolVersion',
  'needsToVerifyTerms',
  'notesDidMigrateToCloudKitOnMac',
  'notesDidFinishMigrationToCloudKit',
  'notesIsUsingCloudKit',
  'notesMigrated',
  'AuthenticationScheme',
  'SSLEnabled',
  'StoreSentMessagesOnServer',
  'StoreTrashOnServer',
  'StoreArchiveOnServer',
  'MFServerSSLCertificateIsTrusted',
  'StoreDraftsOnServer',

  'mergedPrivacyAcknowledgements',
  'privacyAcknowledgement',
  'storefrontID',
  'inGoodStanding', --idk?
  'didAgreeToTerms',
  'self-handle',
  --'bBBundleRef',
  'status',
  'hasOptionalTerms',
  'remindersMigrated',
  'primaryEmailVerified',
  'isCloudSubscriber',
  'remindersAutoMigratableToCK',
  'remindersIsUsingCloudKit',
  'remindersDidFinishMigrationToCloudKit',
  'biometricsState',
  'pushRegistrationThrottleMap',
  'availableServiceTypes',
  'kind',
  'scope',
  'isNewCustomer',
  'enabledServiceTypes',
  'lastAuthenticateCredentialSource',
  'repair-state',
  'repairState',
  'silentEscrowRecordRepairEnabled',
  'silentEscrowRecordRepairEnabledV2',
  --'rRRetaining-services',
  'com.apple.ak.checkin-allowed',
  'auth-mode',
  'appleIdSignInEnabled',
  'usesCloudDocs',
  'security-level',
  'vettedPrimaryEmail',
  'retaining-services',
  'primaryAccount', -- CAN BE AXED, ACCOUNT CLASS WILL PROBABLY CONTAIN THIS TOO
  'accountClass', -- IDK
  'Class', -- JUST TYPE OF ACCOUNT
  'bundleRef',
  'AccountPath',
  'privacyAcknowledgement',
  'canHaveBeneficiary',
  'canBeBeneficiary',
  'canBeCustodian',
  'canHaveCustodian',
  'familyEligible',
  'NotesNotificationPrefix', --YAHOO RELATED
  'NotesPushedMailboxes', --YAHOO RELATED
  'PushedMailboxes', --YAHOO RELATED
  'GKCredentialScope-5',
  'playerID', --GAMECENTER, JUST SEEMS TO BE DSI D
  'personID', --ICLOUD, JUST SEEMS TO BE DSI D
  'profile-id', -- MESSAGES AND APPLEid JUST SEEMS TO BE DSI D

  --NEEDS TESTING
  'cookies',
  'lastAuthenticationServerResponse',
  'accountFlags',
  'registerSuccessCriteria',

  -- FAKE, DOESNT EXIST, DO NOT REMOVE. DUPE OF PHONEnUMBERS WITH STARS INSTEAD OF NUMBERS
  'obfuscatedPhoneNumbers',
  'silenBurnMiniBuddyEnabled' -- fake, doesnt exist, do not remove. 
);

DELETE FROM ZACCOUNT
WHERE ZPARENTACCOUNT IS NOT NULL;


-- deleting child accounts

DROP TABLE IF EXISTS "ZACCESSOPTIONSKEY";
--DROP TABLE IF EXISTS "ZACCOUNT";
--DROP TABLE IF EXISTS "ZACCOUNTPROPERTY";
--DROP TABLE IF EXISTS "ZACCOUNTTYPE";
DROP TABLE IF EXISTS "ZAUTHORIZATION";
DROP TABLE IF EXISTS "ZCREDENTIALITEM";
DROP TABLE IF EXISTS "ZDATACLASS";

-- strip mac data classes
DROP TABLE IF EXISTS "Z_1OWNINGACCOUNTTYPES";
DROP TABLE IF EXISTS "Z_2ENABLEDDATACLASSES";
DROP TABLE IF EXISTS "Z_2PROVISIONEDDATACLASSES";
DROP TABLE IF EXISTS "Z_4SUPPORTEDDATACLASSES";
DROP TABLE IF EXISTS "Z_4SYNCABLEDATACLASSES";
DROP TABLE IF EXISTS "Z_METADATA";
DROP TABLE IF EXISTS "Z_MODELCACHE";
DROP TABLE IF EXISTS "Z_PRIMARYKEY";

COMMIT;

VACUUM;