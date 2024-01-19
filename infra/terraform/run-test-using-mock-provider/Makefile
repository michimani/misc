.PHONY: tfdocs tftest-mod

tfdocs:
	find ./modules -type d -not -path "./modules" -not -path "./modules/*/.terraform*" -not -path "./modules/*/tests" -exec sh -c 'cd "{}" && terraform-docs markdown table --output-file README.md --output-mode inject .' \;
	find ./environments -type d -not -path "./environments" -not -path "./environments/*/.terraform*" -not -path "./environments/*/tests" -exec sh -c 'cd "{}" && terraform-docs markdown table --output-file README.md --output-mode inject .' \;

tftest-mod:
	find ./modules -type d -not -path "./modules" -not -path "./modules/*/.terraform*" -not -path "./modules/*/tests" -exec sh -c 'cd "{}" && terraform test' \;