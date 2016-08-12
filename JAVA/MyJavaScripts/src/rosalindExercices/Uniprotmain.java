package rosalindExercices;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

public class Uniprotmain {
	public static void main(String[] args) throws IOException {

		// Open an read file
		String fileName = "/home/guillermo/Escritorio/Script/myScripts/Rosalind/IDlist.txt";
		File file = new File(fileName);
		BufferedReader br = new BufferedReader(new FileReader(file));
		String line;
		Access newentry;
		List<Access> idList = new ArrayList<>();
		while ((line = br.readLine()) != null) {
			// System.out.println(line);
			newentry = new Access(line);
			idList.add(newentry);
		}//end while
		br.close();

		//connect to Uniprot server
		retrieveFromUniprot(idList);

		//search the motifs

		for (Access id : idList) {
			char[] fasta;
			fasta = id.getFasta().toCharArray();
			for (int i = 0; i < fasta.length; i++) {

				if(fasta[i]=='N' && fasta[i+1]!='P' && (fasta[i+2]=='S' || fasta[i+2]=='T') && fasta[i+3] != 'P'){
					id.addToMotifs(i+1);
				}//end if

			}//end for
			if (!id.motifs.isEmpty()) {
			System.out.println(id.Id);
			System.out.println(id.motifs);
			}
		}//end for

	}//end main

	private static void retrieveFromUniprot(List<Access> idList) throws MalformedURLException, IOException {
		URL myURL;
		for (Access entry : idList){
			String url= "http://www.uniprot.org/uniprot/";
			url = url + entry.Id + ".fasta";
			System.out.println(url);
			myURL = new URL(url);
		    URLConnection myURLConnection = myURL.openConnection();
		    BufferedReader urlReader = new BufferedReader(new InputStreamReader(myURLConnection.getInputStream()));
		    String urlLine;
		    //Read the uniprot info
		    StringBuilder fastaSeq = new StringBuilder();
		    while ((urlLine = urlReader.readLine()) != null){
		    	if (urlLine.startsWith(">")) {
					entry.setHeader(urlLine);
				}else{
					fastaSeq.append(urlLine);
				}
		    	}//end while
		    	entry.setFasta(fastaSeq.toString());

		}//end for
	}//end retrieveFromUniprot
}//end Uniprot
