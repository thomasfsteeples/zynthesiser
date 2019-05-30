// Generated from /Users/steeps/Documents/CDT-Courses/Mini-Project-1/tsynth/tsynth/grammars/SyGuS_lexer_rules.g4 by ANTLR 4.7.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class SyGuS_lexer_rules extends Lexer {
	static { RuntimeMetaData.checkVersion("4.7.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		LEFT_PARENS=1, RIGHT_PARENS=2, SYMBOL=3, QUOTED_LITERAL=4, POSITIVE_INT_CONST=5, 
		NEGATIVE_INT_CONST=6, REAL_CONST=7, BOOL_CONST=8, BV_CONST=9, COMMENT=10, 
		WHITESPACE=11, NEWLINE=12;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	public static final String[] ruleNames = {
		"LEFT_PARENS", "RIGHT_PARENS", "SYMBOL", "QUOTED_LITERAL", "POSITIVE_INT_CONST", 
		"NEGATIVE_INT_CONST", "REAL_CONST", "BOOL_CONST", "BV_CONST", "COMMENT", 
		"WHITESPACE", "NEWLINE", "LOWERCASE_LETTER", "UPPERCASE_LETTER", "SPECIAL_CHAR", 
		"DIGIT", "BINARY_DIGIT", "HEXADECIMAL_DIGIT"
	};

	private static final String[] _LITERAL_NAMES = {
		null, "'('", "')'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, "LEFT_PARENS", "RIGHT_PARENS", "SYMBOL", "QUOTED_LITERAL", "POSITIVE_INT_CONST", 
		"NEGATIVE_INT_CONST", "REAL_CONST", "BOOL_CONST", "BV_CONST", "COMMENT", 
		"WHITESPACE", "NEWLINE"
	};
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public SyGuS_lexer_rules(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "SyGuS_lexer_rules.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\16\u00a3\b\1\4\2"+
		"\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4"+
		"\13\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22"+
		"\t\22\4\23\t\23\3\2\3\2\3\3\3\3\3\4\3\4\3\4\5\4/\n\4\3\4\3\4\3\4\3\4\7"+
		"\4\65\n\4\f\4\16\48\13\4\3\5\3\5\3\5\3\5\3\5\6\5?\n\5\r\5\16\5@\3\5\3"+
		"\5\3\6\6\6F\n\6\r\6\16\6G\3\7\3\7\6\7L\n\7\r\7\16\7M\3\b\5\bQ\n\b\3\b"+
		"\6\bT\n\b\r\b\16\bU\3\b\3\b\6\bZ\n\b\r\b\16\b[\3\t\3\t\3\t\3\t\3\t\3\t"+
		"\3\t\3\t\3\t\5\tg\n\t\3\n\3\n\3\n\3\n\6\nm\n\n\r\n\16\nn\3\n\3\n\3\n\3"+
		"\n\3\n\6\nv\n\n\r\n\16\nw\5\nz\n\n\3\13\3\13\7\13~\n\13\f\13\16\13\u0081"+
		"\13\13\3\13\5\13\u0084\n\13\3\13\3\13\3\13\3\13\3\f\6\f\u008b\n\f\r\f"+
		"\16\f\u008c\3\f\3\f\3\r\5\r\u0092\n\r\3\r\3\r\3\r\3\r\3\16\3\16\3\17\3"+
		"\17\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\177\2\24\3\3\5\4\7\5\t\6"+
		"\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\2\35\2\37\2!\2#\2%\2\3\2"+
		"\t\4\2\13\13\"\"\3\2c|\3\2C\\\n\2##&(,-/\61>A`a~~\u0080\u0080\3\2\62;"+
		"\3\2\62\63\4\2CHch\2\u00b4\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2"+
		"\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2"+
		"\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\3\'\3\2\2\2\5)\3\2\2\2\7.\3\2\2"+
		"\2\t9\3\2\2\2\13E\3\2\2\2\rI\3\2\2\2\17P\3\2\2\2\21f\3\2\2\2\23y\3\2\2"+
		"\2\25{\3\2\2\2\27\u008a\3\2\2\2\31\u0091\3\2\2\2\33\u0097\3\2\2\2\35\u0099"+
		"\3\2\2\2\37\u009b\3\2\2\2!\u009d\3\2\2\2#\u009f\3\2\2\2%\u00a1\3\2\2\2"+
		"\'(\7*\2\2(\4\3\2\2\2)*\7+\2\2*\6\3\2\2\2+/\5\33\16\2,/\5\35\17\2-/\5"+
		"\37\20\2.+\3\2\2\2.,\3\2\2\2.-\3\2\2\2/\66\3\2\2\2\60\65\5\33\16\2\61"+
		"\65\5\35\17\2\62\65\5!\21\2\63\65\5\37\20\2\64\60\3\2\2\2\64\61\3\2\2"+
		"\2\64\62\3\2\2\2\64\63\3\2\2\2\658\3\2\2\2\66\64\3\2\2\2\66\67\3\2\2\2"+
		"\67\b\3\2\2\28\66\3\2\2\29>\7$\2\2:?\5\33\16\2;?\5\35\17\2<?\5!\21\2="+
		"?\7\60\2\2>:\3\2\2\2>;\3\2\2\2><\3\2\2\2>=\3\2\2\2?@\3\2\2\2@>\3\2\2\2"+
		"@A\3\2\2\2AB\3\2\2\2BC\7$\2\2C\n\3\2\2\2DF\5!\21\2ED\3\2\2\2FG\3\2\2\2"+
		"GE\3\2\2\2GH\3\2\2\2H\f\3\2\2\2IK\7/\2\2JL\5!\21\2KJ\3\2\2\2LM\3\2\2\2"+
		"MK\3\2\2\2MN\3\2\2\2N\16\3\2\2\2OQ\7/\2\2PO\3\2\2\2PQ\3\2\2\2QS\3\2\2"+
		"\2RT\5!\21\2SR\3\2\2\2TU\3\2\2\2US\3\2\2\2UV\3\2\2\2VW\3\2\2\2WY\7\60"+
		"\2\2XZ\5!\21\2YX\3\2\2\2Z[\3\2\2\2[Y\3\2\2\2[\\\3\2\2\2\\\20\3\2\2\2]"+
		"^\7v\2\2^_\7t\2\2_`\7w\2\2`g\7g\2\2ab\7h\2\2bc\7c\2\2cd\7n\2\2de\7u\2"+
		"\2eg\7g\2\2f]\3\2\2\2fa\3\2\2\2g\22\3\2\2\2hi\7%\2\2ij\7d\2\2jl\3\2\2"+
		"\2km\5#\22\2lk\3\2\2\2mn\3\2\2\2nl\3\2\2\2no\3\2\2\2oz\3\2\2\2pq\7%\2"+
		"\2qr\7z\2\2ru\3\2\2\2sv\5!\21\2tv\5%\23\2us\3\2\2\2ut\3\2\2\2vw\3\2\2"+
		"\2wu\3\2\2\2wx\3\2\2\2xz\3\2\2\2yh\3\2\2\2yp\3\2\2\2z\24\3\2\2\2{\177"+
		"\7=\2\2|~\13\2\2\2}|\3\2\2\2~\u0081\3\2\2\2\177\u0080\3\2\2\2\177}\3\2"+
		"\2\2\u0080\u0083\3\2\2\2\u0081\177\3\2\2\2\u0082\u0084\7\17\2\2\u0083"+
		"\u0082\3\2\2\2\u0083\u0084\3\2\2\2\u0084\u0085\3\2\2\2\u0085\u0086\7\f"+
		"\2\2\u0086\u0087\3\2\2\2\u0087\u0088\b\13\2\2\u0088\26\3\2\2\2\u0089\u008b"+
		"\t\2\2\2\u008a\u0089\3\2\2\2\u008b\u008c\3\2\2\2\u008c\u008a\3\2\2\2\u008c"+
		"\u008d\3\2\2\2\u008d\u008e\3\2\2\2\u008e\u008f\b\f\2\2\u008f\30\3\2\2"+
		"\2\u0090\u0092\7\17\2\2\u0091\u0090\3\2\2\2\u0091\u0092\3\2\2\2\u0092"+
		"\u0093\3\2\2\2\u0093\u0094\7\f\2\2\u0094\u0095\3\2\2\2\u0095\u0096\b\r"+
		"\2\2\u0096\32\3\2\2\2\u0097\u0098\t\3\2\2\u0098\34\3\2\2\2\u0099\u009a"+
		"\t\4\2\2\u009a\36\3\2\2\2\u009b\u009c\t\5\2\2\u009c \3\2\2\2\u009d\u009e"+
		"\t\6\2\2\u009e\"\3\2\2\2\u009f\u00a0\t\7\2\2\u00a0$\3\2\2\2\u00a1\u00a2"+
		"\t\b\2\2\u00a2&\3\2\2\2\26\2.\64\66>@GMPU[fnuwy\177\u0083\u008c\u0091"+
		"\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}