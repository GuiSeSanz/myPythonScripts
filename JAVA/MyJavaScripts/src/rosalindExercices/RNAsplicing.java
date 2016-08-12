package rosalindExercices;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.Map.Entry;

import org.biojava.nbio.core.sequence.DNASequence;
import org.biojava.nbio.core.sequence.ProteinSequence;
import org.biojava.nbio.core.sequence.compound.AminoAcidCompound;
import org.biojava.nbio.core.sequence.compound.AminoAcidCompoundSet;
import org.biojava.nbio.core.sequence.io.FastaReader;
import org.biojava.nbio.core.sequence.io.FastaReaderHelper;
import org.biojava.nbio.core.sequence.io.GenericFastaHeaderParser;
import org.biojava.nbio.core.sequence.io.ProteinSequenceCreator;

public class RNAsplicing {
	public static void main(String[] args) throws IOException {
		File fastaFile = new File("/home/guillermo/Escritorio/Script/myScripts/Rosalind/rosalind_cons1.txt");
		LinkedHashMap<String, DNASequence> fastaReader = FastaReaderHelper.readFastaDNASequence(fastaFile);
		for (Entry<String, DNASequence> fastaEntry : fastaReader.entrySet()){
			System.out.println(fastaEntry.getValue().getOriginalHeader() + "=" + fastaEntry.getValue().getSequenceAsString());
			System.out.println(fastaEntry.getValue().getGCCount()/(double)fastaEntry.getValue().getLength() * 100);
		}

	}// end main


		   public static void OpenFasta(String[] args) throws Exception{
		       /*
		        * Method 1: With the FastaReaderHelper
		        */
		       //Try with the FastaReaderHelper
		       LinkedHashMap<String, ProteinSequence> a = FastaReaderHelper.readFastaProteinSequence(new File(args[0]));
		       //FastaReaderHelper.readFastaDNASequence for DNA sequences

		       for (  Entry<String, ProteinSequence> entry : a.entrySet() ) {
		           System.out.println( entry.getValue().getOriginalHeader() + "=" + entry.getValue().getSequenceAsString() );
		       }

		       /*
		        * Method 2: With the FastaReader Object
		        */
		       //Try reading with the FastaReader
		       FileInputStream inStream = new FileInputStream( args[0] );
		       FastaReader<ProteinSequence,AminoAcidCompound> fastaReader =
		           new FastaReader<ProteinSequence,AminoAcidCompound>(
		                   inStream,
		                   new GenericFastaHeaderParser<ProteinSequence,AminoAcidCompound>(),
		                   new ProteinSequenceCreator(AminoAcidCompoundSet.getAminoAcidCompoundSet()));
		       LinkedHashMap<String, ProteinSequence> b = fastaReader.process();
		       for (  Entry<String, ProteinSequence> entry : b.entrySet() ) {
		           System.out.println( entry.getValue().getOriginalHeader() + "=" + entry.getValue().getSequenceAsString() );
		       }
		   }

		}

