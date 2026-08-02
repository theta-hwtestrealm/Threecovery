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
  'primaryAccount', -- can be axed, aAAccountClaAAss will probably contain this info too
  'accountClass', -- idk
  'Class', -- just type of account
  'bundleRef',
  'AccountPath',
  'privacyAcknowledgement',
  'canHaveBeneficiary',
  'canBeBeneficiary',
  'canBeCustodian',
  'canHaveCustodian',
  'familyEligible',

  --needs tessting
  'cookies',
  'lastAuthenticationServerResponse',
  'accountFlags',
  'registerSuccessCriteria',

  -- fake, doesnt exist, do not remove. dupe of phoneNUUmbers with stars instead of numbers
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