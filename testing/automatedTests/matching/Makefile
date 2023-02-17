# This Makefile compiles the cpp program that analyzes the matching results

main:
	g++ analyzeResults.cpp utilities.cpp -o bin/analyzeResults
	g++ findTotalNumCorrectMatches.cpp -o bin/countMatches

clean:
	@rm bin/analyzeResults bin/countMatches 2>/dev/null || true
	@rm -rf lisFiles/ 2>/dev/null || true
	@rm -rf mindtctXyt/ minutiaeOutXyt/ 2>/dev/null || true
	@rm -rf matchingResults/ 2>/dev/null || true
